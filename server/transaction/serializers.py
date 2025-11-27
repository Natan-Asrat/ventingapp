from rest_framework import serializers
from .models import Transaction, Subscription

class TransactionsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class SubscriptionsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['is_active', 'amount', 'product_code_internal', 'product_name', 'current_period_end', 'formatted_current_period_end', 'days_left', 'recurring_interval', 'recurring_interval_count']