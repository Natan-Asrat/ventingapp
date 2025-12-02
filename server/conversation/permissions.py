from rest_framework import permissions
from .models import Member, Message

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


class IsActiveConversationMemberForConvAfterId(permissions.BasePermission):
    """
    Allows access only to users who are members of the conversation.
    """
    def has_permission(self, request, view):
        after_id = request.query_params.get("after_id")
        if not after_id:
            return False
        try:
            after_id = int(after_id)
        except ValueError:
            return False
        
        return Member.objects.filter(
            conversation_id=after_id,
            user=request.user
        ).exists()

class IsActiveConversationMemberForConvBulk(permissions.BasePermission):
    """
    Allows access only if the user is a member of ALL conversations in the list.
    """
    def has_permission(self, request, view):
        ids = request.query_params.get("id")
        if not ids:
            return False

        try:
            id_list = [int(i) for i in ids.split(",") if i.isdigit()]
        except ValueError:
            return False

        if not id_list:
            return False

        # Check if there exists ANY conversation in the list
        # that does NOT have this user as an active member
        member_count = Member.objects.filter(
            conversation_id__in=id_list,
            user=request.user,
            is_active=True
        ).values("conversation_id").distinct().count()

        # MUST match all conversations requested
        return member_count == len(id_list)

class IsActiveConversationMemberForMessageBulk(permissions.BasePermission):
    """
    Only allow bulk message access if the user is a member of ALL conversations
    that these messages belong to.
    """
    def has_permission(self, request, view):
        ids = request.query_params.get("id")
        if not ids:
            return False

        try:
            id_list = [int(i) for i in ids.split(",") if i.isdigit()]
        except ValueError:
            return False

        if not id_list:
            return False

        # 1. Get distinct conversations from message IDs
        conversation_ids = (
            Message.objects
            .filter(id__in=id_list)
            .values_list("conversation_id", flat=True)
            .distinct()
        )

        # Convert to list to safely use len()
        conv_list = list(conversation_ids)

        # 2. Count how many of those conversations the user is an active member of
        member_count = (
            Member.objects
            .filter(
                conversation_id__in=conv_list,
                user=request.user,
                is_active=True
            )
            .values("conversation_id")
            .distinct()
            .count()
        )

        # User must be a member of ALL conversations
        return member_count == len(conv_list)
