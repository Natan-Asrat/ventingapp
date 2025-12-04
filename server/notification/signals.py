from report.models import ReportDecision, ReportTypes
from post.models import Post
from account.models import Connection
from conversation.models import Message
from .models import Notification
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=ReportDecision)
def create_notification(sender, instance, created, **kwargs):
    if created:
        if instance.report.report_type == ReportTypes.TRANSACTION:
            Notification.objects.create(
                report_decision=instance,
                title="Admin Decision",
                message=instance.reason,
                user=instance.report.about_user,
                viewed=False
            )
        elif instance.report.report_type == ReportTypes.POST and instance.approved:
            post = instance.report.reported_post
            post.banned = True
            post.save()
            Notification.objects.create(
                report_decision=instance,
                title="Admin Decision",
                message=instance.reason,
                user=instance.report.reported_by,
                viewed=False
            )
        elif instance.report.report_type == ReportTypes.POST and instance.rejected:
            post = instance.report.reported_post
            post.banned = False
            post.save()
            Notification.objects.create(
                report_decision=instance,
                title="Admin Decision",
                message=instance.reason,
                user=instance.report.reported_by,
                viewed=False
            )
        elif instance.report.report_type == ReportTypes.CONNECTION and instance.approved:
            connection = instance.report.reported_connection
            connection.banned = True
            connection.save()
            Notification.objects.create(
                report_decision=instance,
                title="Admin Decision",
                message=instance.reason,
                user=instance.report.reported_by,
                viewed=False
            )
        elif instance.report.report_type == ReportTypes.CONNECTION and instance.rejected:
            connection = instance.report.reported_connection
            connection.banned = False
            connection.save()
            Notification.objects.create(
                report_decision=instance,
                title="Admin Decision",
                message=instance.reason,
                user=instance.report.reported_by,
                viewed=False
            )
        elif instance.report.report_type == ReportTypes.MESSAGE and instance.approved:
            message = instance.report.reported_message
            connection = message.conversation.connection
            connection.banned = True
            connection.save()
            message.banned = True
            message.save()
            Notification.objects.create(
                report_decision=instance,
                title="Admin Decision",
                message=instance.reason,
                user=instance.report.reported_by,
                viewed=False
            )
        elif instance.report.report_type == ReportTypes.MESSAGE and instance.rejected:
            message = instance.report.reported_message
            message.banned = False
            message.save()
            connection = message.conversation.connection
            connection.banned = False
            connection.save()
            Notification.objects.create(
                report_decision=instance,
                title="Admin Decision",
                message=instance.reason,
                user=instance.report.reported_by,
                viewed=False
            )


@receiver(pre_save, sender=Post)
def post_banned(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        previous = sender.objects.get(pk=instance.pk)
        prev_banned = previous.banned
    except sender.DoesNotExist:
        prev_banned = False
    report_decision = None
    try:
        report_decision = ReportDecision.objects.filter(
            report__reported_post=instance,
            approved=True,
        ).order_by('-created_at').first()
    except ReportDecision.DoesNotExist:
        report_decision = None
    if instance.banned and not prev_banned and report_decision:

        Notification.objects.create(
            title="Post Banned",
            message="Your post has been banned!",
            user=instance.posted_by,
            report_decision=report_decision,
        )


@receiver(pre_save, sender=Post)
def post_unbanned(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        previous = sender.objects.get(pk=instance.pk)
        prev_banned = previous.banned
    except sender.DoesNotExist:
        prev_banned = False
    report_decision = None
    try:
        report_decision = ReportDecision.objects.filter(
            report__reported_post=instance,
            approved=True,
        ).order_by('-created_at').first()
    except ReportDecision.DoesNotExist:
        report_decision = None
    if not instance.banned and prev_banned and report_decision:

        Notification.objects.create(
            title="Post Unbanned",
            message="Your post has been unbanned!",
            user=instance.posted_by,
            report_decision=report_decision,
        )

@receiver(pre_save, sender=Connection)
def connection_banned(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        previous = sender.objects.get(pk=instance.pk)
        prev_banned = previous.banned
    except sender.DoesNotExist:
        prev_banned = False
    report_decision = None
    try:
        report_decision = ReportDecision.objects.filter(
            report__reported_connection=instance,
            approved=True,
        ).order_by('-created_at').first()
    except ReportDecision.DoesNotExist:
        report_decision = None
    if instance.banned and not prev_banned and report_decision:

        Notification.objects.create(
            title="Connection Banned",
            message="Your connection has been banned!",
            user=instance.initiating_user,
            report_decision=report_decision,
        )

@receiver(pre_save, sender=Connection)
def connection_unbanned(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        previous = sender.objects.get(pk=instance.pk)
        prev_banned = previous.banned
    except sender.DoesNotExist:
        prev_banned = False
    report_decision = None
    try:
        report_decision = ReportDecision.objects.filter(
            report__reported_connection=instance,
            approved=True,
        ).order_by('-created_at').first()
    except ReportDecision.DoesNotExist:
        report_decision = None
    if not instance.banned and prev_banned and report_decision:

        Notification.objects.create(
            title="Connection Unbanned",
            message="Your connection has been unbanned!",
            user=instance.initiating_user,
            report_decision=report_decision,
        )

@receiver(pre_save, sender=Message)
def message_banned(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        previous = sender.objects.get(pk=instance.pk)
        prev_banned = previous.banned
    except sender.DoesNotExist:
        prev_banned = False
    report_decision = None
    try:
        report_decision = ReportDecision.objects.filter(
            report__reported_message=instance,
            approved=True,
        ).order_by('-created_at').first()
    except ReportDecision.DoesNotExist:
        report_decision = None
    if instance.banned and not prev_banned and report_decision:

        Notification.objects.create(
            title="Message Banned",
            message="Your message was found to be inappropriate and has been banned!",
            user=instance.user,
            report_decision=report_decision,
        )

@receiver(pre_save, sender=Message)
def message_unbanned(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        previous = sender.objects.get(pk=instance.pk)
        prev_banned = previous.banned
    except sender.DoesNotExist:
        prev_banned = False
    report_decision = None
    try:
        report_decision = ReportDecision.objects.filter(
            report__reported_message=instance,
            approved=True,
        ).order_by('-created_at').first()
    except ReportDecision.DoesNotExist:
        report_decision = None
    if not instance.banned and prev_banned and report_decision:

        Notification.objects.create(
            title="Message Unbanned",
            message="Your message has been unbanned!",
            user=instance.user,
            report_decision=report_decision,
        )