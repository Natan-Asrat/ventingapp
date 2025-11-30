from rest_framework import viewsets, mixins
from .models import ConnectUsage
from .serializers import ConnectUsageSerializer
from account.pagination import CustomPagination

# Create your views here.
class ConnectUsageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ConnectUsage.objects.all().select_related('connection', 'connection__connected_user', 'connection__initiating_user').order_by('-created_at')
    serializer_class = ConnectUsageSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)