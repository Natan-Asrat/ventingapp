from rest_framework import serializers
from .models import Transaction

class TransactionsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'