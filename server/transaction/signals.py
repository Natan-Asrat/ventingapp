from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Transaction

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
            if hasattr(user, "connects"):
                print("user connects before", user.connects)
                user.connects = (user.connects or 0) + transaction_connects
                user.save(update_fields=["connects"])
                print("updated user connects to", user.connects)
