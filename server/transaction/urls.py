from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, ManualPaymentViewSet
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'manual_payments', ManualPaymentViewSet)
urlpatterns = router.urls