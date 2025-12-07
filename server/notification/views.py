from rest_framework import viewsets, mixins
from .models import Notification
from .serializers import NotificationSerializer
from .query import optimize_notification_queryset
from .pagination import NotificationPagination
# Create your views here.
class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = optimize_notification_queryset(Notification.objects.all().order_by("-created_at"))
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
