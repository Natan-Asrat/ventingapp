from django.db import models
from server.utils import get_readable_time_since
# Create your models here.
class ConnectUsage(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    connectsSpent = models.IntegerField(default=0)
    connectsBefore = models.IntegerField(default=0)
    connectsAfter = models.IntegerField(default=0)
    connection = models.ForeignKey('account.Connection', on_delete=models.SET_NULL, null=True, blank=True)
    transaction = models.ForeignKey('transaction.Transaction', on_delete=models.SET_NULL, null=True, blank=True)
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
        return f"{self.user} - {self.connectsSpent}"
    
from .signals import *