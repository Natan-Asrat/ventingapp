from django.db import models
from server.utils import get_readable_time_since

class PaymentMethods:
    POLAR = "POLAR"
    STRIPE = "STRIPE"


class Customer(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)
    customer_id = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    tax_id = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('transaction.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    subscription_id = models.TextField()
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    product_code_internal = models.CharField(max_length=255, blank=True, null=True)
    product_id = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)

    recurring_interval = models.TextField(blank=True, null=True)
    recurring_interval_count = models.IntegerField(blank=True, null=True)

    # Subscription periods
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    
    # Optional trial fields
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def formatted_current_period_end(self):
        return self.current_period_end.strftime("%B %d, %Y")

    @property
    def days_left(self):
        return get_readable_time_since(self.current_period_end)


class ManualPaymentOption(models.Model):
    created_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='manual_payment_option_created')
    logo = models.ImageField(upload_to='manual_payment_option/logo/', blank=True, null=True)
    method = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    nameOnAccount = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.method
    
class Transaction(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    subscription = models.ForeignKey('transaction.Subscription', on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey('transaction.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    method = models.CharField(max_length=255)

    manual_payment_option = models.ForeignKey('transaction.ManualPaymentOption', on_delete=models.SET_NULL, blank=True, null=True)

    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    refunded_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    discount_id = models.TextField(blank=True, null=True) 
    invoice_number = models.CharField(max_length=255, blank=True, null=True
    )
    is_invoice_generated = models.BooleanField(default=False)

    is_payment_required = models.BooleanField(default=True)
    connects = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    
    requires_approval = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=255)
    billing_name = models.TextField(blank=True, null=True)

    celebrated = models.BooleanField(default=False)
    

    screenshot = models.ImageField(upload_to='screenshot/', blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)
    
    product_id = models.TextField(blank=True, null=True)
    product_code_internal = models.CharField(max_length=255, blank=True, null=True)    
    product_name = models.TextField(blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    
    reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from .signals import *