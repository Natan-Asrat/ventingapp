from .models import Message, Reaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from post.recommendation import update_user_interests, get_activity_weight
from django.conf import settings

@receiver(post_save, sender=Message)
def update_reply_count(sender, instance, created, **kwargs):
    if created:
        print("instance", instance.__dict__)
        # reply count
        if instance.reply_to:
            instance.reply_to.reply_count += 1
            instance.reply_to.save()
        # forward count
        if instance.forwarded_from:
            instance.forwarded_from.forward_count += 1
            instance.forwarded_from.save()

@receiver(post_save, sender=Reaction)
def update_reaction_count(sender, instance, created, **kwargs):
    if created:
        instance.message.reaction_count += 1
        instance.message.save()

@receiver(post_save, sender=Message)
def new_shared_post(sender, instance, created, **kwargs):
    post = instance.shared_post
    user = instance.user

    if created and post is not None and user.id != post.posted_by.id and post.embedding is not None:
        update_user_interests(
            user, 
            post, 
            weight=get_activity_weight(settings.POST_ACTIVITY_TYPES.SEND_POST)
        )