from account.models import Connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ConnectUsage

@receiver(post_save, sender=Connection)
def new_connection(sender, instance, created, **kwargs):
    if created:
        connects_before = instance.initiating_user.connects
        connects_spent = instance.connectSpent
        instance.connected_user.connects += connects_spent
        instance.initiating_user.connects -= connects_spent
        instance.connected_user.save()
        instance.initiating_user.save()
        ConnectUsage.objects.create(
            user=instance.initiating_user,
            connectsBefore=connects_before,
            connectsSpent=connects_spent,
            connectsAfter=instance.initiating_user.connects,
            connection=instance
        )