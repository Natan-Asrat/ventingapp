from django.db import models
from server.utils import get_readable_time_since

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    report_decision = models.ForeignKey('report.ReportDecision', on_delete=models.SET_NULL, null=True, blank=True)
    viewed = models.BooleanField(default=False)
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
        report_decision = "- Report Decision: " + str(self.report_decision) if self.report_decision else ""
        return f"Notification #{self.pk} for {self.user} - {self.title} {report_decision}"

from .signals import *