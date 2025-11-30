from rest_framework import viewsets, mixins
from .models import Notification
from .serializers import NotificationSerializer
# Create your views here.
class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.all().order_by("-created_at").select_related("report_decision", "report_decision__report", "report_decision__report__reported_post", "report_decision__report__reported_connection", "report_decision__report__reported_transaction", "report_decision__report__reported_post__posted_by").prefetch_related("report_decision__report__reported_post__payment_info_list")
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
