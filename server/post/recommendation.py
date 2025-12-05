

from django.db import transaction
from django.db.models import Case, IntegerField, OuterRef, Exists, Value, When
from .models import ClusterMember, PreviousRecommendedPost, Post, UserInterest
from pgvector.django import CosineDistance
from django.conf import settings
from scipy.spatial.distance import cosine
from numpy import array as np_array

def get_activity_weight(activity):
    return settings.POST_ACTIVITY_WEIGHTS.get(activity, 1)


def update_user_interests(user, post, weight=1.0):
    clusters = list(UserInterest.objects.filter(user=user))
    embedding = post.embedding

    if not clusters:
        new_cluster = UserInterest.objects.create(
            user=user,
            centroid=embedding,
            count=weight,
            radius=0.0
        )
        ClusterMember.objects.create(centroid=new_cluster, post=post, weight=weight)
        return new_cluster


    # Ensure embeddings are numpy arrays
    embedding = np_array(embedding)

    # Compute cosine distance to all clusters
    distances = [(c, cosine(embedding, np_array(c.centroid))) for c in clusters]
    closest, dist = min(distances, key=lambda x: x[1])

    # Dynamic threshold
    threshold = max(closest.radius * 1.5, 0.30)

    # Too far → create new cluster
    if dist > threshold:
        new_cluster = UserInterest.objects.create(
            user=user,
            centroid=embedding,
            count=weight,
            radius=0.0
        )
        ClusterMember.objects.create(centroid=new_cluster, post=post, weight=weight)
        return new_cluster

    # Weighted update
    old_centroid = np_array(closest.centroid)
    old_count = closest.count
    alpha = weight / (old_count + weight)

    new_centroid = (old_centroid * (1 - alpha)) + (embedding * alpha)
    new_radius = max(closest.radius, float(dist))

    closest.centroid = new_centroid.tolist()  # store as list in DB
    closest.radius = new_radius
    closest.count = old_count + weight
    closest.save(update_fields=["centroid", "radius", "count"])

    cm, created = ClusterMember.objects.get_or_create(
        centroid=closest,
        post=post,
        defaults={"weight": weight}
    )
    if not created:
        cm.weight += weight
        cm.save(update_fields=["weight"])


    return closest

def get_top_post_ids(user, post_count = settings.TOP_POSTS_RECOMMENDED_COUNT):
    """
    Returns a list of post IDs for a user in the desired order:
    - Top 5 interests by count, posts per interest: 5,4,3,2,1
    - Randomly include posts from other interests to fill up
    - Excludes posts created by the user or previously recommended
    """
    selected_ids = []

    # Annotate posts that were previously recommended
    previously_recommended = PreviousRecommendedPost.objects.filter(
        post_id=OuterRef('pk'),
        user=user
    )

    # Top 5 interests by count
    top_interests = list(UserInterest.objects.filter(user=user).order_by('-count')[:settings.TOP_K_INTERESTS])
    # Top 5 interests
    for i, interest in enumerate(top_interests):
        num_posts = settings.TOP_K_INTERESTS_POST_RETURNED_COUNT[i]
        qs = Post.objects.filter(
            archived=False, banned=False, embedding__isnull=False
        ).exclude(id__in=selected_ids).exclude(posted_by=user).annotate(
            previously_recommended=Exists(previously_recommended),
            similarity=CosineDistance('embedding', interest.centroid)
        ).filter(previously_recommended=False, similarity__lte=settings.COSINE_THRESHOLD).order_by('similarity')[:num_posts]
        selected_ids.extend(list(qs.values_list('id', flat=True)))

    # Random interests outside top 5 (fill remaining slots)
    remaining_needed = post_count - len(selected_ids)
    if remaining_needed > 0:
        remaining_interests = UserInterest.objects.filter(user=user).exclude(id__in=[i.id for i in top_interests]).order_by('?')
        for interest in remaining_interests:
            if len(selected_ids) >= post_count:
                break
            qs = Post.objects.filter(
                archived=False, banned=False, embedding__isnull=False
            ).exclude(id__in=selected_ids).exclude(posted_by=user).annotate(
                previously_recommended=Exists(previously_recommended),
                similarity=CosineDistance('embedding', interest.centroid)
            ).filter(previously_recommended=False, similarity__lte=settings.COSINE_THRESHOLD).order_by('?')[:remaining_needed]
            selected_ids.extend(list(qs.values_list('id', flat=True)))
            remaining_needed = post_count - len(selected_ids)
        
    
    # Fallback: top posts by views if still not enough
    remaining_needed = post_count - len(selected_ids)
    if remaining_needed > 0:
        qs = Post.objects.filter(
            archived=False, banned=False
        ).exclude(id__in=selected_ids).annotate(
            previously_recommended=Exists(previously_recommended),
            is_own_post=Case(
                When(posted_by=user, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('previously_recommended', '-views', 'is_own_post')[:remaining_needed]
        remaining_ids = list(qs.values_list('id', flat=True))
        selected_ids.extend(remaining_ids)

    # Bulk create PreviousRecommendedPost
    posts_to_create = [PreviousRecommendedPost(post_id=pid, user=user) for pid in selected_ids]
    if posts_to_create:
        with transaction.atomic():
            PreviousRecommendedPost.objects.bulk_create(posts_to_create, ignore_conflicts=True)

    return selected_ids


def updated_post_view_count(post, user):
    if user.id != post.posted_by.id and post.embedding is not None:
        update_user_interests(
            user, 
            post, 
            weight=get_activity_weight(settings.POST_ACTIVITY_TYPES.VIEW_POST)
        )