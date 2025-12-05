from .models import Comment, Like, LikeComment, Post, PostView, Save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .embed import get_embedding
from .recommendation import update_user_interests, get_activity_weight
from django.conf import settings

@receiver(post_save, sender=Post)
def new_post(sender, instance, created, **kwargs):
    if created and not instance.embedding:
        embedding = get_embedding(instance.description)
        print("embedded", instance.description)
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
