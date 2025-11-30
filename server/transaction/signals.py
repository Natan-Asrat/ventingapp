from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction
from .utils import add_connects, add_signup_free_connects
from usage.models import ConnectUsage
from account.models import User
from django.utils import timezone
from django.conf import settings

@receiver(pre_save, sender=Transaction)
def add_connects_on_approval(sender, instance: Transaction, **kwargs):
    print("transaction signal", instance.transaction_id)
    try:
        previous = sender.objects.get(pk=instance.pk)
        prev_approved = previous.approved
    except sender.DoesNotExist:
        prev_approved = False

    print("prev_approved", prev_approved)
    print("instance.approved", instance.approved)

    if not prev_approved and instance.approved:
        user = instance.user
        if user:
            transaction_connects = instance.connects or 0
            connects_before = user.connects
            add_connects(transaction_connects, user)
            ConnectUsage.objects.create(
                user=user,
                connectsBefore=connects_before,
                connectsSpent=transaction_connects,
                connectsAfter=user.connects,
                transaction=instance
            )


@receiver(post_save, sender=User)
def free_signup_connects(sender, instance, created, **kwargs):
    if created:
        add_signup_free_connects(instance)