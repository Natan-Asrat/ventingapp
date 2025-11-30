from .models import ConnectUsage
from rest_framework import serializers
from account.serializers import ConnectionListSerializer
from transaction.serializers import TransactionsSimpleSerializer
class ConnectUsageSerializer(serializers.ModelSerializer):
    connection = ConnectionListSerializer()
    transaction = TransactionsSimpleSerializer()
    class Meta:
        model = ConnectUsage
        fields = '__all__'
