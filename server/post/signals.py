from .models import Comment, Like, LikeComment, PaymentInfo, Post, PostView, Save
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .embed import get_embedding
from .recommendation import update_user_interests, get_activity_weight
from django.conf import settings 
from account.models import Connection

@receiver(post_save, sender=Post)
def new_post(sender, instance, created, **kwargs):
    if created and not instance.embedding:
        embedding = get_embedding(instance.description)
        Post.objects.filter(id=instance.id).update(embedding=embedding)

@receiver(post_save, sender=Like)
def new_like(sender, instance, created, **kwargs):
    post = instance.post
    user = instance.liked_by

    if created and user.id != post.posted_by.id and instance.active and post.embedding is not None:
        update_user_interests(
            user, 
            post, 
            weight=get_activity_weight(settings.POST_ACTIVITY_TYPES.LIKE_POST)
        )

@receiver(post_save, sender=Comment)
def new_comment(sender, instance, created, **kwargs):
    post = instance.post
    user = instance.commented_by
    
    if created and user.id != post.posted_by.id and post.embedding is not None:
        if instance.reply_to:
            update_user_interests(
                user, 
                post, 
                weight=get_activity_weight(settings.POST_ACTIVITY_TYPES.REPLY_COMMENT)
            )
        else:
            update_user_interests(
                user, 
                post, 
                weight=get_activity_weight(settings.POST_ACTIVITY_TYPES.COMMENT_POST)
            )

@receiver(post_save, sender=LikeComment)
def new_comment_like(sender, instance, created, **kwargs):
    post = instance.comment.post
    user = instance.liked_by

    if created and user.id != post.posted_by.id and post.embedding is not None:
        update_user_interests(
            user, 
            post, 
            weight=get_activity_weight(settings.POST_ACTIVITY_TYPES.LIKE_COMMENT)
        )

@receiver(post_save, sender=Save)
def new_save(sender, instance, created, **kwargs):
    post = instance.post
    user = instance.saved_by

    if created and user.id != post.posted_by.id and post.embedding is not None:
        update_user_interests(
            user, 
            post, 
            weight=get_activity_weight(settings.POST_ACTIVITY_TYPES.SAVE_POST)
        )

from .cache import (
    update_user_post_bitstring, 
    sync_connection_cache_by_ids,
    update_post_data
)

@receiver([post_save, post_delete], sender=Like)
def handle_like_change(sender, instance, **kwargs):
    # instance.liked_by is your user relation, instance.post is your post relation
    if not settings.CACHE_ENABLED: return
    update_user_post_bitstring(instance.liked_by_id, instance.post_id)

@receiver([post_save, post_delete], sender=Save)
def handle_save_change(sender, instance, **kwargs):
    # instance.saved_by is your user relation
    if not settings.CACHE_ENABLED: return
    update_user_post_bitstring(instance.saved_by_id, instance.post_id)


@receiver([post_save, post_delete], sender=Connection)
def handle_connection_change(sender, instance, **kwargs):
    if not settings.CACHE_ENABLED: return
    sync_connection_cache_by_ids(instance.initiating_user_id, instance.connected_user_id)

@receiver(post_save, sender=Post)
def handle_post_update(sender, instance, **kwargs):
    if not settings.CACHE_ENABLED: return
    update_post_data(instance.id)

@receiver([post_save, post_delete], sender=PaymentInfo)
def handle_payment_info_update(sender, instance, **kwargs):
    if not settings.CACHE_ENABLED: return
    update_post_data(instance.post_id)