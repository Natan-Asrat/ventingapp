from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Transaction
from .utils import add_connects

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
            add_connects(transaction_connects, user)