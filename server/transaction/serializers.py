from rest_framework import serializers
from .models import Transaction, Subscription, ManualPaymentOption
from django.conf import settings
from urllib.parse import urljoin
class TransactionsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

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
