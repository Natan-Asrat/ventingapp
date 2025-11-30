from rest_framework.routers import DefaultRouter
from .views import ConnectUsageViewSet
router = DefaultRouter()
router.register(r'connect-usages', ConnectUsageViewSet)
urlpatterns = router.urls