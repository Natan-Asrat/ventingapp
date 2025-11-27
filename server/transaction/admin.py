from django.contrib import admin
from .models import Transaction, Customer, Subscription, ManualPaymentOption
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(ManualPaymentOption)