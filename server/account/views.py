from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from .models import User
from .serializers import UserCreateSerializer, UserSimpleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .utils import send_email_otp, verify_email_otp
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewset(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                send_email_otp(user)
                return Response(
                    UserSimpleSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if verify_email_otp(user, otp):
            return Response(
                {"message": "Email verified successfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def send_reset_otp(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        send_email_otp(user, "Reset Password Code")
        return Response(
            {"message": "OTP sent successfully"},
            status=status.HTTP_200_OK
        )


    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_reset_otp(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not verify_email_otp(user, otp):
            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken.for_user(user)
        print("refresh", refresh)
        access_token = str(refresh.access_token)

        return Response({"access": access_token}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def reset_password(self, request):
        user = request.user
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        if password1 != password2:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(password1)
        user.save()
        return Response(
            {"message": "Password reset successfully"},
            status=status.HTTP_200_OK
        )
            

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def resend_otp(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.email_verified:
            return Response(
                {"error": "Email already verified!"},
                status=status.HTTP_404_NOT_FOUND
            )
        send_email_otp(user)
        return Response(
            {"message": "OTP sent successfully"},
            status=status.HTTP_200_OK
        )


    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
