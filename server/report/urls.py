from rest_framework.routers import DefaultRouter
from .views import ReportDecisionViewSet, ReportViewSet, AppealViewSet
router = DefaultRouter()
router.register(r'report-decisions', ReportDecisionViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'appeals', AppealViewSet)

urlpatterns = router.urls