from rest_framework import viewsets, mixins
from .models import Notification
from .serializers import NotificationSerializer
# Create your views here.
class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.all().order_by("-created_at")
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
