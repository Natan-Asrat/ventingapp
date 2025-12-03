from django.db import models
from server.utils import get_readable_time_since
class ReportTypes:
    POST = "post"
    CONNECTION = "connection"
    TRANSACTION = "transaction"
    CONVERSATION = "conversation"
    MESSAGE = "message"

# Create your models here.
class Report(models.Model):
    report_type_options = [
        (ReportTypes.POST, "Post"),
        (ReportTypes.CONNECTION, "Connection"),
        (ReportTypes.TRANSACTION, "Transaction"),
        (ReportTypes.CONVERSATION, "Conversation"),
        (ReportTypes.MESSAGE, "Message"),
    ]
    
    reason = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    about_user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_about')

    report_type = models.CharField(max_length=255, blank=True, null=True, choices=report_type_options)
    concluded = models.BooleanField(default=False)
    dismissed = models.BooleanField(default=False)
    
    reported_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_sent')
    reported_post = models.ForeignKey('post.Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    reported_connection = models.ForeignKey('account.Connection', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    reported_transaction = models.ForeignKey('transaction.Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    reported_message = models.ForeignKey('conversation.Message', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y")
    
    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%B %d, %Y")
    
    @property
    def created_since(self):
        return get_readable_time_since(self.created_at)

    @property
    def updated_since(self):
        return get_readable_time_since(self.updated_at)
    


    def __str__(self):
        reported_by_str = self.reported_by.username if self.reported_by else "System"
        return f"Report #{self.pk} by {reported_by_str} on {self.about_user}"

class ReportDecision(models.Model):
    report = models.ForeignKey('report.Report', on_delete=models.CASCADE, related_name='decisions')
    decision_maker = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='report_decisions')
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    has_appeals = models.BooleanField(default=False)
    from_appeal = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y")
    
    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%B %d, %Y")
    
    @property
    def created_since(self):
        return get_readable_time_since(self.created_at)

    @property
    def updated_since(self):
        return get_readable_time_since(self.updated_at)
    
    def __str__(self):
        decision = "Approved" if self.approved else "Rejected" if self.rejected else "Pending" 
        return f"Decision #{self.pk} - {decision} - for Report: {self.report}"

class Appeal(models.Model):
    submitted_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_appeals')
    report_decision = models.ForeignKey('report.ReportDecision', on_delete=models.SET_NULL, null=True, blank=True, related_name='appeals')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y")
    
    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%B %d, %Y")
    
    @property
    def created_since(self):
        return get_readable_time_since(self.created_at)

    @property
    def updated_since(self):
        return get_readable_time_since(self.updated_at)

    
    def __str__(self):
        return f"Appeal #{self.pk} by {self.submitted_by} on Report Decision: {self.report_decision}"

    
class AppealDecision(models.Model):
    appeal = models.ForeignKey('report.Appeal', on_delete=models.SET_NULL, null=True, blank=True, related_name='decisions')
    decision_maker = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='appeal_decisions')
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y")
    
    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%B %d, %Y")
    
    @property
    def created_since(self):
        return get_readable_time_since(self.created_at)

    @property
    def updated_since(self):
        return get_readable_time_since(self.updated_at)
    
    def __str__(self):
        decision = "Approved" if self.approved else "Rejected" if self.rejected else "Pending" 
        return f"Appeal Decision #{self.pk} - {decision} - for Appeal: {self.appeal}"


from .signals import *