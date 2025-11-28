from report.models import ReportDecision
from .models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=ReportDecision)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            report_decision=instance,
            title="Admin Decision",
            message=instance.reason,
            user=instance.report.about_user,
            viewed=False
        )