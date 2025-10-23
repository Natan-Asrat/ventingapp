from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewset, CustomTokenObtainPairView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh")
]