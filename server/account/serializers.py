from rest_framework import serializers
from .models import User


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
        fields = ["email", "username", "name", "connects", "profile_picture"]