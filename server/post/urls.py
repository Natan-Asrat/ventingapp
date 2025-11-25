from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, PaymentInfoViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'payment_info', PaymentInfoViewSet)

urlpatterns = [
    path('', include(router.urls))
]