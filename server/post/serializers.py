from rest_framework import serializers
from .models import Post, PaymentInfo, Comment, Like, Save
from account.serializers import UserSimpleSerializer

class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = ['method', 'account', 'nameOnAccount']


class PostCreateSerializer(serializers.ModelSerializer):
    payment_info = PaymentInfoSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['description', 'image', 'payment_info']

    def create(self, validated_data):
        payment_info_data = validated_data.pop('payment_info', [])
        post = Post.objects.create(**validated_data)

        if payment_info_data:
            PaymentInfo.objects.bulk_create([
                PaymentInfo(post=post, **info) for info in payment_info_data
            ])

        return post

class PostSimpleSerializer(serializers.ModelSerializer):
    posted_by = UserSimpleSerializer()
    payment_info_list = PaymentInfoSerializer(many=True, read_only=True)
    liked = serializers.BooleanField(read_only=True)
    saved = serializers.BooleanField(read_only=True)
    connected = serializers.BooleanField(read_only=True)
    rejected_connection = serializers.BooleanField(read_only=True)
    pending_connection = serializers.BooleanField(read_only=True)
    removed_connection = serializers.BooleanField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'posted_by', 'connected', 'rejected_connection', 'pending_connection', 'removed_connection', 'description', 'image', 'liked', 'saved', 'likes', 'comments', 'saves', 'views', 'payment_info_list', 'formatted_created_at', 'formatted_updated_at', 'created_at', 'updated_at', 'archived']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message']
    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value

class LikedPostsSerializer(serializers.ModelSerializer):
    post = PostSimpleSerializer()
    class Meta:
        model = Like
        fields = ['post', 'formatted_created_at', 'formatted_updated_at', 'created_at', 'updated_at', 'active']

class SavedPostsSerializer(serializers.ModelSerializer):
    post = PostSimpleSerializer()
    class Meta:
        model = Save
        fields = ['post', 'formatted_created_at', 'formatted_updated_at', 'created_at', 'updated_at', 'active']

class CommentsOnPostSerializer(serializers.ModelSerializer):
    commented_by = UserSimpleSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'message', 'commented_by', 'likes', 'replies', 'formatted_created_at', 'formatted_updated_at', 'created_at', 'updated_at', 'archived']

class RepliesSerializer(serializers.ModelSerializer):
    commented_by = UserSimpleSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'message', 'commented_by', 'likes', 'replies', 'formatted_created_at', 'formatted_updated_at', 'created_at', 'updated_at', 'archived']