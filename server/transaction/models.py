from django.db import models
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    subscription = models.ForeignKey('transaction.Subscription', on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey('transaction.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    method = models.CharField(max_length=255)

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
    

    screenshot = models.ImageField(upload_to='screenshot/', blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)
    
    product_id = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
