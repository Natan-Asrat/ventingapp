from rest_framework import serializers
from .models import User, Connection

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
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

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password1')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "name", "connects", "profile_picture"]

class ConnectionListSerializer(serializers.ModelSerializer):
    connected_user = UserSimpleSerializer()
    iniating_user = UserSimpleSerializer()
    class Meta:
        model = Connection
        fields = ["id", "iniating_user", "connected_user", "connectSpent", "created_at", "updated_at", "removed", "reported", "reconnection_count", "reconnection_rejected", "formatted_created_at", "formatted_updated_at"]