from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from conversation.models import Message
from .models import AppealDecision, Report, ReportDecision, Appeal
from .serializers import ReportDecisionSerializer, AppealsAndDecisionsSerializer, ReportsWithDecisionsSerializer
from .permissions import IsReportAboutOrStaff
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from post.models import Post
from .models import ReportTypes
from account.permissions import IsConnectedUser
from account.models import Connection

class ReportViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Report.objects.all().prefetch_related(
            'decisions',
            "reported_post__payment_info_list",
            "reported_message__shared_post__payment_info_list"
        ).order_by(
            "-created_at"
        ).select_related(
            "reported_post", 
            "reported_connection", 
            "reported_transaction", 
            "reported_post__posted_by",
            "reported_message",
            "reported_message__user",
            "reported_message__forwarded_from",
            "reported_message__reply_to",
            "reported_message__shared_post",
            "reported_message__shared_post__posted_by",
            "reported_message__forwarded_from__user",
            "reported_message__reply_to__user"
        )
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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def report_post(self, request):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({'error': 'Post ID is required'}, status=400)
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
        existing_report = Report.objects.filter(
            reported_by=request.user,
            reported_post=post,
            report_type=ReportTypes.POST,
        ).first()
        if existing_report:
            return Response({'error': 'You have already reported this post'}, status=400)
        
        Report.objects.create(
            reported_by=request.user,
            about_user=post.posted_by,
            reported_post=post,
            reason=request.data.get('reason'),
            report_type=ReportTypes.POST,
        )
        return Response(status=200)

    @action(detail=False, methods=['post'], permission_classes=[IsConnectedUser])
    def report_connection(self, request):
        connection_id = request.data.get('connection_id')
        if not connection_id:
            return Response({'error': 'Connection ID is required'}, status=400)
        try:
            connection = Connection.objects.get(id=connection_id)
        except Connection.DoesNotExist:
            return Response({'error': 'Connection not found'}, status=404)
        existing_report = Report.objects.filter(
            reported_by=request.user,
            reported_connection=connection,
            report_type=ReportTypes.CONNECTION,
        ).first()
        if existing_report:
            return Response({'error': 'You have already reported this connection'}, status=400)
        
        Report.objects.create(
            reported_by=request.user,
            about_user=connection.initiating_user,
            reported_connection=connection,
            reason=request.data.get('reason'),
            report_type=ReportTypes.CONNECTION,
        )
        return Response(status=200)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def report_message(self, request):
        message_id = request.data.get('message_id')
        if not message_id:
            return Response({'error': 'Message ID is required'}, status=400)
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=404)
        existing_report = Report.objects.filter(
            reported_by=request.user,
            reported_message=message,
            report_type=ReportTypes.MESSAGE,
        ).first()
        if existing_report:
            return Response({'error': 'You have already reported this message'}, status=400)
        
        Report.objects.create(
            reported_by=request.user,
            about_user=message.user,
            reported_message=message,
            reason=request.data.get('reason'),
            report_type=ReportTypes.MESSAGE,
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
    
