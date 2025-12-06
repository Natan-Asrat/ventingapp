from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from account.models import User
from post.models import PostView
from transaction.models import Transaction
from django.utils import timezone
from django.db.models import Sum


class AnalyticsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin_dashboard(self, request):
        today = timezone.now().date()

        user_count = User.objects.count()
        daily_active_users = PostView.objects.filter(
            updated_at__date=today
        ).values('user').distinct().count()
        total_revenue = Transaction.objects.filter(approved=True).aggregate(
            total=Sum('usd_equivalent')
        )['total'] or 0
        return Response({
            "user_count": user_count,
            "daily_active_users": daily_active_users,
            "total_revenue": total_revenue
        }, status=status.HTTP_200_OK)

