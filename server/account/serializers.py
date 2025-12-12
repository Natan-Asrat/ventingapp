from rest_framework import serializers
from .models import User, Connection
from urllib.parse import urljoin
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from server.image import validate_and_clean_image

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No account found with this email."})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Oops! Wrong password. Try again."})

        return super().validate(attrs)

class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "name", "profile_picture", "password1", "password2"]

    def validate(self, data):
        if data.get("password1") != data.get("password2"):
            raise serializers.ValidationError({
                "password": "Passwords must match!"
            })
        if User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError({
                "email": "A user with this email already exists!"
            })

        if User.objects.filter(username=data.get("username")).exists():
            raise serializers.ValidationError({
                "username": "A user with this username already exists!"
            })
        
        return data
    def validate_profile_picture(self, value):
        if value:
            return validate_and_clean_image(value)
        return None

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password1')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class UserSimpleSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "email", "username", "name", "connects", "profile_picture", "date_joined", "formatted_date_joined", "date_joined_since", "is_staff"]
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            absolute_url =  urljoin(settings.BACKEND_URL, obj.profile_picture.url)
            return absolute_url
        return None

class ConnectionListSerializer(serializers.ModelSerializer):
    connected_user = UserSimpleSerializer()
    initiating_user = UserSimpleSerializer()
    class Meta:
        model = Connection
        fields = ["id", "initiating_user", "banned", "message", "connected_user", "connectSpent", "created_at", "updated_at", "removed", "reported", "reconnection_count", "reconnection_rejected", "reconnection_requested_by", "formatted_created_at", "formatted_updated_at"]

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "profile_picture"]
        extra_kwargs = {
            "name": {"required": False},
            "profile_picture": {"required": False},
        }

    def validate(self, attrs):
        name = attrs.get("name")
        picture = attrs.get("profile_picture")

        if not name and not picture:
            raise serializers.ValidationError("Provide either name or profile_picture.")

        # Prevent updating both at once — UI sends only one at a time
        if name and picture:
            raise serializers.ValidationError("You can update only one field at a time.")

        return attrs

    def update(self, instance, validated_data):
        name = validated_data.get("name")
        picture = validated_data.get("profile_picture")

        if name:
            instance.name = name
        if picture:
            instance.profile_picture = picture

        instance.save()
        return instance
    def validate_profile_picture(self, value):
        if value:
            return validate_and_clean_image(value)
        return None

class OtherProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    followers = serializers.IntegerField()
    connected = serializers.BooleanField()
    rejected_connection = serializers.BooleanField()
    banned_connection = serializers.BooleanField()
    pending_connection = serializers.BooleanField()
    removed_connection = serializers.BooleanField()
    class Meta:
        model = User
        fields = [
            "id", 
            "post_likes", 
            "username", 
            "name", 
            "profile_picture", 
            "date_joined", 
            "formatted_date_joined", 
            "date_joined_since",
            "followers", 
            "connected",
            "rejected_connection",
            "banned_connection",
            "pending_connection",
            "removed_connection"
        ]
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            absolute_url =  urljoin(settings.BACKEND_URL, obj.profile_picture.url)
            return absolute_url
        return None
    # def get_followers(self, obj):
    #     return Connection.objects.filter(connected_user=obj, removed=False).count()

    # def get_connected(self, obj):
    #     request = self.context.get("request")
    #     user = request.user
    #     return Connection.objects.filter(
    #         Q(initiating_user=user, connected_user=obj) |
    #         Q(initiating_user=obj, connected_user=user),
    #         removed=False
    #     ).exists()

    # def get_pending_connection(self, obj):
    #     request = self.context.get("request")
    #     user = request.user
    #     return Connection.objects.filter(
    #         Q(initiating_user=user, connected_user=obj) |
    #         Q(initiating_user=obj, connected_user=user),
    #         reconnection_requested=True,
    #         removed=True,
    #         reconnection_rejected=False
    #     ).exists()
    
    # def get_rejected_connection(self, obj):
    #     request = self.context.get("request")
    #     user = request.user
    #     return Connection.objects.filter(
    #         Q(initiating_user=user, connected_user=obj) |
    #         Q(initiating_user=obj, connected_user=user),
    #         removed=True,
    #         reconnection_rejected=True
    #     ).exists()

    # def get_banned_connection(self, obj):
    #     request = self.context.get("request")
    #     user = request.user
    #     return Connection.objects.filter(
    #         Q(initiating_user=user, connected_user=obj) |
    #         Q(initiating_user=obj, connected_user=user),
    #         banned=True
    #     ).exists()
    
    # def get_removed_connection(self, obj):
    #     request = self.context.get("request")
    #     user = request.user
    #     return Connection.objects.filter(
    #         Q(initiating_user=user, connected_user=obj) |
    #         Q(initiating_user=obj, connected_user=user),
    #         removed=True,
    #     ).exists()
