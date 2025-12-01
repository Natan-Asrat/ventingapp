from rest_framework import serializers
from django.conf import settings
from urllib.parse import urljoin
from account.serializers import UserSimpleSerializer
from .models import Conversation, Member, Message, Reaction

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'category', 'created_at', 'updated_at']

class OtherMemberSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    class Meta:
        model = Member
        fields = ['id', 'user', 'created_at', 'updated_at']

class ConversationSimpleSerializer(serializers.ModelSerializer):
    my_membership_list = MemberSerializer(many=True)
    other_user_list = OtherMemberSerializer(many=True)
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'name', 'logo', 'is_group', 'my_membership_list', 'other_user_list', 'members_count', 'active', 'created_at', 'updated_at']
    def get_logo(self, obj):
        if obj.logo:
            absolute_url =  urljoin(settings.BACKEND_URL, obj.logo.url)
            return absolute_url
        return None

class ReplySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    class Meta:
        model = Message
        fields = ['id', 'message', 'user', 'created_at']

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'reaction', 'created_at']

class OthersReactionSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    class Meta:
        model = Reaction
        fields = ['id', 'reaction', 'user', 'created_at']

class MessageSimpleSerializer(serializers.ModelSerializer):
    reply_to = ReplySerializer()
    my_reaction_list = ReactionSerializer(many=True)
    other_reactions_list = OthersReactionSerializer(many=True)
    user = UserSimpleSerializer()
    class Meta:
        model = Message
        fields = ['id', 'user', 'message', 'my_reaction_list', 'other_reactions_list', 'reply_to', 'reaction_count', 'reply_count', 'view_count', 'created_at', 'updated_at']

