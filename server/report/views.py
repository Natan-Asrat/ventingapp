from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser
from .models import AppealDecision, Report, ReportDecision, Appeal
from .serializers import ReportDecisionSerializer, AppealsAndDecisionsSerializer, ReportsWithDecisionsSerializer
from .permissions import IsReportAboutOrStaff
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ReportViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Report.objects.all().prefetch_related('decisions').order_by("-created_at")
    serializer_class = ReportsWithDecisionsSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        report = self.get_object()
        report.dismissed = True
        report.save()
        return Response(status=200)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        report = self.get_object()
        report.concluded = True
        report.save()
        ReportDecision.objects.create(
            report=report,
            decision_maker=request.user,
            approved=True,
            rejected=False,
            reason=request.data.get('reason')
        )
        return Response(status=200)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        report = self.get_object()
        report.concluded = True
        report.save()
        ReportDecision.objects.create(
            report=report,
            decision_maker=request.user,
            approved=False,
            rejected=True,
            reason=request.data.get('reason')
        )
        return Response(status=200)

# Create your views here.
class ReportDecisionViewSet(viewsets.GenericViewSet):
    queryset = ReportDecision.objects.all()
    serializer_class = ReportDecisionSerializer
    permission_classes = [IsReportAboutOrStaff]

    def get_queryset(self):
        if self.action == 'list':
            return ReportDecision.objects.filter(report__about_user=self.request.user)
        elif self.action == 'submit_appeal':
            return ReportDecision.objects.filter(from_appeal=False)
        return super().get_queryset()

    @action(detail=True, methods=['post'])
    def submit_appeal(self, request, pk=None):
        report_decision = self.get_object()
        report_decision.has_appeals = True
        report_decision.save()
        message = request.data.get('message')
        Appeal.objects.create(
            submitted_by = request.user,
            report_decision = report_decision,
            message=message
        )
        return Response(status=200)

    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def appeals(self, request, pk=None):
        report_decision = self.get_object()
        appeals = Appeal.objects.filter(report_decision=report_decision).prefetch_related('decisions', 'decisions__decision_maker').select_related('submitted_by')
        serializer = AppealsAndDecisionsSerializer(appeals, many=True)
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=['get'])
    def my_appeals(self, request, pk=None):
        report_decision = self.get_object()
        appeals = Appeal.objects.filter(report_decision=report_decision, submitted_by=request.user).prefetch_related('decisions', 'decisions__decision_maker').select_related('submitted_by')
        serializer = AppealsAndDecisionsSerializer(appeals, many=True)
        return Response(serializer.data, status=200)

class AppealViewSet(viewsets.GenericViewSet):
    queryset = Appeal.objects.all()
    serializer_class = AppealsAndDecisionsSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        appeal = self.get_object()
        AppealDecision.objects.create(
            appeal=appeal,
            decision_maker=request.user,
            approved=True,
            rejected=False,
            reason=request.data.get('reason')
        )

        return Response(status=200)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        appeal = self.get_object()
        AppealDecision.objects.create(
            appeal=appeal,
            decision_maker=request.user,
            approved=False,
            rejected=True,
            reason=request.data.get('reason')
        )
        return Response(status=200)
    
