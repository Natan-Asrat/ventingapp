from rest_framework import serializers
from .models import Report, ReportDecision, Appeal, AppealDecision
from account.serializers import UserSimpleSerializer
from transaction.serializers import TransactionsSimpleSerializer
from post.serializers import PostSimpleSerializer
class ReportSerializer(serializers.ModelSerializer):
    reported_transaction = TransactionsSimpleSerializer()
    reported_post = PostSimpleSerializer()
    class Meta:
        model = Report
        fields = [
            'id', 
            'reason', 
            'active', 
            'report_type', 
            'created_at', 
            'updated_at', 
            'about_user', 
            'reported_post', 
            'reported_connection', 
            'reported_transaction',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]

class ReportDecisionSerializer(serializers.ModelSerializer):
    report = ReportSerializer()
    class Meta:
        model = ReportDecision
        fields = [
            'id', 
            'report', 
            'decision_maker', 
            'has_appeals',
            'from_appeal',
            'approved', 
            'rejected', 
            'reason', 
            'created_at', 
            'updated_at',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]

class AppealDecisionSimpleSerializer(serializers.ModelSerializer):
    decision_maker = UserSimpleSerializer()
    class Meta:
        model = AppealDecision
        fields = [
            'id',
            'decision_maker',
            'approved',
            'rejected',
            'reason',
            'created_at',
            'updated_at',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]
class AppealsAndDecisionsSerializer(serializers.ModelSerializer):
    decisions = AppealDecisionSimpleSerializer(many=True)
    submitted_by = UserSimpleSerializer()
    class Meta:
        model = Appeal
        fields = [
            'id', 
            'report_decision', 
            'decisions',
            'submitted_by', 
            'message', 
            'created_at', 
            'updated_at',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]

class ReportDecisionAndAppealsSerializer(serializers.ModelSerializer):
    appeals = AppealsAndDecisionsSerializer(many=True)
    class Meta:
        model = ReportDecision
        fields = [
            'id', 
            'report', 
            'appeals',
            'decision_maker', 
            'has_appeals',
            'approved', 
            'rejected', 
            'reason', 
            'created_at', 
            'updated_at',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]

class ReportDecisionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDecision
        fields = [
            'id', 
            'report', 
            'decision_maker', 
            'approved', 
            'rejected', 
            'has_appeals',
            'reason', 
            'created_at', 
            'updated_at',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]


class ReportsWithDecisionsAndAppealsSerializer(serializers.ModelSerializer):
    reported_transaction = TransactionsSimpleSerializer()
    decisions = ReportDecisionAndAppealsSerializer(many=True)
    class Meta:
        model = Report
        fields = [
            'id', 
            'reason', 
            'decisions',
            'active', 
            'report_type', 
            'created_at', 
            'updated_at', 
            'about_user', 
            'reported_by', 
            'reported_post', 
            'reported_connection', 
            'reported_transaction',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]

class ReportsWithDecisionsSerializer(serializers.ModelSerializer):
    reported_transaction = TransactionsSimpleSerializer()
    reported_post = PostSimpleSerializer()
    decisions = ReportDecisionSimpleSerializer(many=True)
    class Meta:
        model = Report
        fields = [
            'id', 
            'reason', 
            'decisions',
            'active', 
            'report_type', 
            'created_at', 
            'updated_at', 
            'about_user', 
            'reported_by', 
            'reported_post', 
            'reported_connection', 
            'reported_transaction',
            'formatted_created_at',
            'formatted_updated_at',
            'created_since',
            'updated_since'
        ]
