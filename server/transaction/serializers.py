from rest_framework import serializers
from .models import Transaction, Subscription, ManualPaymentOption
from django.conf import settings
from urllib.parse import urljoin
class TransactionsSimpleSerializer(serializers.ModelSerializer):
    screenshot_url = serializers.SerializerMethodField()    
    class Meta:
        model = Transaction
        fields = [
            'pk',
            'method', 
            'product_name', 
            'subscription', 
            'manual_payment_option', 
            'subtotal_amount', 
            'total_amount', 
            'net_amount', 
            'tax_amount', 
            'discount_amount', 
            'refunded_amount', 
            'refunded_tax_amount', 
            'discount_id', 
            'invoice_number', 
            'is_invoice_generated', 
            'is_payment_required', 
            'connects', 
            'currency', 
            'requires_approval', 
            'approved', 
            'status', 
            'billing_name', 
            'celebrated',
            'transaction_id',
            'screenshot_url',
            'created_at',
            'formatted_created_at',
            'time_ago'
        ]
    
    def get_screenshot_url(self, obj):
        if obj.screenshot:
            absolute_url =  urljoin(settings.BACKEND_URL, obj.screenshot.url)
            return absolute_url
        return None

class SubscriptionsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['is_active', 'amount', 'product_code_internal', 'product_name', 'current_period_end', 'formatted_current_period_end', 'days_left', 'recurring_interval', 'recurring_interval_count']

class ManualPaymentOptionSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    class Meta:
        model = ManualPaymentOption
        fields = ['pk', 'method', 'account', 'nameOnAccount', 'active', 'currency', 'exchange_rate', 'logo_url']

    def get_logo_url(self, obj):
        if obj.logo:
            absolute_url =  urljoin(settings.BACKEND_URL, obj.logo.url)
            return absolute_url
        return None
