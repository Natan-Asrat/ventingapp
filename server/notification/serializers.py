from rest_framework import serializers
from .models import Notification
from report.serializers import ReportDecisionSerializer

class NotificationSerializer(serializers.ModelSerializer):
    report_decision = ReportDecisionSerializer()
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'title',
            'message',
            'report_decision',
            'viewed',
            'created_at',
            'updated_at',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]