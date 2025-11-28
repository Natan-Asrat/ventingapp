from .models import AppealDecision, Report, ReportTypes, ReportDecision
from transaction.models import ManualPaymentDecision
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=ManualPaymentDecision)
def create_report(sender, instance, created, **kwargs):
    if created:
        report = Report.objects.create(
            report_type=ReportTypes.TRANSACTION,
            reason=instance.reason,
            about_user=instance.transaction.user,
            reported_transaction=instance.transaction,
            concluded=True,
            dismissed = False
        )
        ReportDecision.objects.create(
            report=report,
            decision_maker=instance.decision_maker,
            approved=instance.approved,
            rejected=instance.rejected,
            reason=instance.reason
        )

@receiver(post_save, sender=AppealDecision)
def approve_appeal(sender, instance, created, **kwargs):
    if created and instance.approved:
        report_decision = instance.appeal.report_decision
        report = report_decision.report
        ReportDecision.objects.create(
            report=report,
            decision_maker=instance.decision_maker,
            approved=instance.approved,
            rejected=instance.rejected,
            reason=instance.reason,
            from_appeal=True
        )
        transaction = report.reported_transaction

        if transaction and transaction.rejected:
            transaction.approved = True
            transaction.rejected = False
            transaction.save()

@receiver(post_save, sender=AppealDecision)
def reject_appeal(sender, instance, created, **kwargs):
    if created and instance.rejected:
        report_decision = instance.appeal.report_decision
        report = report_decision.report
        ReportDecision.objects.create(
            report=report,
            decision_maker=instance.decision_maker,
            approved=instance.approved,
            rejected=instance.rejected,
            reason=instance.reason,
            from_appeal=True
        )
        transaction = report.reported_transaction

        if transaction and transaction.approved:
            transaction.approved = False
            transaction.rejected = True
            transaction.save()
