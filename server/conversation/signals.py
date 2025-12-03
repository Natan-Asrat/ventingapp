from .models import Message, Reaction
from django.db.models.signals import post_save
from django.dispatch import receiver


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