from rest_framework import permissions
from .models import Member

class IsActiveConversationMember(permissions.BasePermission):
    """
    Allows access only to users who are active members of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is the Conversation instance
        return Member.objects.filter(
            conversation=obj,
            user=request.user,
            is_active=True
        ).exists()

class IsActiveConversationMemberForMessage(permissions.BasePermission):
    """
    Allows access only to users who are members of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is the Conversation instance
        return Member.objects.filter(
            conversation=obj.conversation,
            user=request.user
        ).exists()