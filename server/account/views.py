from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from .models import User, Connection
from .serializers import (
    UserCreateSerializer, 
    UserSimpleSerializer, 
    ConnectionListSerializer, 
    CustomTokenObtainPairSerializer,
    EditProfileSerializer,
    OtherProfileSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .utils import send_email_otp, verify_email_otp
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q, F
from rest_framework_simplejwt.views import TokenObtainPairView
from .pagination import CustomPagination
from .query import get_other_profile_queryset

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewset(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer
    pagination_class = CustomPagination

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
    
    @action(
        detail=False,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        url_path="edit_profile"
    )
    def edit_profile(self, request):
        serializer = EditProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            UserSimpleSerializer(request.user).data,
            status=status.HTTP_200_OK
        )


    @action(detail=True, methods=['post'])
    def connect(self, request, pk=None):
        user_to_connect = self.get_object()
        initiating_user = request.user
        message = request.data.get('message', '').strip() or None

        # Check if active connection exists
        if Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_connect) |
            Q(initiating_user=user_to_connect, connected_user=initiating_user), 
            removed=False
        ).exists():
            return Response(
                {"error": "You are already connected to this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if removed connection exists
        removed_qs = Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_connect) |
            Q(initiating_user=user_to_connect, connected_user=initiating_user),
            removed=True
        )
        if removed_qs.filter(reconnection_count__gt=5).exists():
            return Response(
                {"error": "Reconnection limit reached."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if removed_qs.filter(reconnection_requested=True).exists():
            return Response(
                {"error": "Reconnection request rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if removed_qs.exists():
            # Check if any reconnection has already been requested
            if removed_qs.filter(reconnection_requested=True).exists():
                return Response(
                    {"error": "Reconnection already requested."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update all removed connections with reconnection request
            removed_qs.update(
                reconnection_requested=True,
                reconnection_requested_by=initiating_user,
                message=message
            )
            return Response(
                {"message": "Reconnection request sent successfully."},
                status=status.HTTP_200_OK
            )

        # No existing connection — create new
        Connection.objects.create(
            initiating_user=initiating_user,
            connected_user=user_to_connect,
            message=message
        )

        initiating_user.connects += 1
        user_to_connect.connections += 1
        initiating_user.save()
        user_to_connect.save()
        return Response({"message": "Connection created successfully."}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def disconnect(self, request, pk=None):
        user_to_disconnect = self.get_object()
        initiating_user = request.user
        if not Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_disconnect) |
            Q(initiating_user=user_to_disconnect, connected_user=initiating_user),
            removed=False
        ).exists():
            return Response({"error": "You are not connected to this user."}, status=status.HTTP_400_BAD_REQUEST)
        Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_disconnect) |
            Q(initiating_user=user_to_disconnect, connected_user=initiating_user),
            removed=False
        ).update(removed=True)
        # dont decrement connection count here
        return Response({"message": "Connection deleted successfully."}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def accept_reconnection(self, request, pk=None):
        user_to_reconnect = self.get_object()
        initiating_user = request.user
        if not Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_reconnect) |
            Q(initiating_user=user_to_reconnect, connected_user=initiating_user),
            removed=True,
            reconnection_requested = True,
            reconnection_requested_by = user_to_reconnect,
            reconnection_rejected = False
        ).exists():
            return Response({"error": "There are no requests to reconnect that you can accept."}, status=status.HTTP_400_BAD_REQUEST)
        Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_reconnect) |
            Q(initiating_user=user_to_reconnect, connected_user=initiating_user),
            removed=True,
            reconnection_requested = True,
            reconnection_requested_by = user_to_reconnect,
            reconnection_rejected = False
        ).update(removed=False, reconnection_count=F('reconnection_count') + 1, reconnection_requested=False, reconnection_requested_by=None)

        # dont increment connection count here
        return Response({"message": "Connection reconnected successfully."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reject_reconnection(self, request, pk=None):
        user_to_reconnect = self.get_object()
        initiating_user = request.user
        if not Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_reconnect) |
            Q(initiating_user=user_to_reconnect, connected_user=initiating_user),
            removed=True,
            reconnection_requested = True,
            reconnection_requested_by = user_to_reconnect,
            reconnection_rejected = False
        ).exists():
            return Response({"error": "There are no requests to reconnect that you can reject."}, status=status.HTTP_400_BAD_REQUEST)
        Connection.objects.filter(
            Q(initiating_user=initiating_user, connected_user=user_to_reconnect) |
            Q(initiating_user=user_to_reconnect, connected_user=initiating_user),
            removed=True,
            reconnection_requested = True,
            reconnection_requested_by = user_to_reconnect
        ).update(reconnection_rejected=True)

        # dont decrement connection count here
        return Response({"message": "Reconnection rejected successfully."}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_connections(self, request):
        user = request.user

        qs = Connection.objects.filter(
            Q(initiating_user=user) | Q(connected_user=user)
        ).select_related('initiating_user', 'connected_user').order_by('-reconnection_count', '-updated_at')
        paginated_queryset = self.paginate_queryset(qs)
        if paginated_queryset is not None:
            serializer = ConnectionListSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ConnectionListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def our_connection(self, request, pk=None):
        user = self.get_object()
        connection = Connection.objects.filter(
            Q(initiating_user=user) | Q(connected_user=user)
        ).select_related('initiating_user', 'connected_user').order_by('-reconnection_count', '-updated_at')
        serializer = ConnectionListSerializer(connection, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def connections(self, request):
        user = request.user
        qs = Connection.objects.filter(
            Q(initiating_user=user) | Q(connected_user=user)
        ).select_related('initiating_user', 'connected_user').order_by('-updated_at')
        paginated_queryset = self.paginate_queryset(qs)
        if paginated_queryset is not None:
            serializer = ConnectionListSerializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ConnectionListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def profile(self, request, pk=None):
        current_user = request.user         # viewer
        target_user = self.get_object()     # profile owner

        annotated_user = get_other_profile_queryset(target_user.id, current_user)

        serializer = OtherProfileSerializer(
            annotated_user,
        )

        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def get_profile_by_username(self, request):
        current_user = request.user         # viewer
        try:
            target_user = User.objects.get(username=request.query_params.get("username"))
            annotated_user = get_other_profile_queryset(target_user.id, current_user)

            serializer = OtherProfileSerializer(
                annotated_user,
            )
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)