from django.db.models.functions import Coalesce
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from account.models import Connection, User
from post.models import Post
from .models import Conversation, Member, Message, Reaction, ConversationCategoryOptions, MessageView
from .serializers import ConversationSimpleSerializer, MessageSimpleSerializer
from django.db.models import Q, Count, OuterRef, Prefetch, Subquery, Value
from rest_framework.decorators import action
from rest_framework.response import Response 
from .permissions import (
    IsActiveConversationMember,
    IsActiveConversationMemberForMessage,
    IsActiveConversationMemberForConvAfterId,
    IsActiveConversationMemberForConvBulk,
    IsActiveConversationMemberForMessageBulk
)
from .pagination import CustomMessagesPagination
from .query import add_conversation_details, get_conversation_queryset, get_unread_counts_by_category
from django.utils import timezone
# Create your views here.
class ConversationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Conversation.objects.none()
    serializer_class = ConversationSimpleSerializer
    pagination_class = CustomMessagesPagination
    def get_queryset(self):
        user = self.request.user
        category = self.request.query_params.get("category")
        qs = get_conversation_queryset(user, category)
        return qs.order_by("-updated_at")

    @action(detail=False, methods=["get"])
    def categories(self, request):
        values = [choice[0] for choice in ConversationCategoryOptions.choices]
        return Response(values)

    @action(detail=True, methods=["get"], permission_classes=[IsActiveConversationMember])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        user=request.user
        my_reaction_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_reaction_list"
        )
        other_reactions_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.exclude(user=user).select_related("user").order_by("-created_at")[:3],
            to_attr="other_reactions_list"
        )

        messages = Message.objects.filter(conversation=conversation).prefetch_related(
            my_reaction_prefetch,
            other_reactions_prefetch,
        ).select_related("user", "reply_to", "reply_to__user", "shared_post", "shared_post__posted_by").prefetch_related("shared_post__payment_info_list").order_by("-created_at")
        paginated_messages = self.paginate_queryset(messages)
        if paginated_messages is not None:
            serializer = MessageSimpleSerializer(paginated_messages, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSimpleSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[IsActiveConversationMember])
    def new_messages(self, request, pk=None):
        """
        Fetch messages created after a given message ID.
        Example: GET /chat/conversations/<pk>/new_messages/?after_id=42
        """
        conversation = self.get_object()
        user = request.user
        after_id = request.query_params.get("after_id")

        if not after_id:
            return Response({"error": "Missing 'after_id' query parameter"}, status=400)

        try:
            after_id = int(after_id)
        except ValueError:
            return Response({"error": "Invalid 'after_id' format"}, status=400)

        my_reaction_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_reaction_list"
        )
        other_reactions_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.exclude(user=user).select_related("user").order_by("-created_at")[:3],
            to_attr="other_reactions_list"
        )

        new_messages_qs = Message.objects.filter(
            conversation=conversation,
            id__gt=after_id
        ).prefetch_related(
            my_reaction_prefetch,
            other_reactions_prefetch,
        ).select_related("user", "reply_to", "reply_to__user", "shared_post", "shared_post__posted_by").prefetch_related("shared_post__payment_info_list").order_by("id")
        paginated_messages = self.paginate_queryset(new_messages_qs)
        if paginated_messages is not None:
            serializer = MessageSimpleSerializer(paginated_messages, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSimpleSerializer(new_messages_qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsActiveConversationMember])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        conversation.updated_at = timezone.now()
        conversation.save()
        user = request.user
        message = request.data.get("message")
        reply_to_id = request.data.get("reply_to")
        if not message:
            return Response({"error": "Message is required"}, status=400)
        if reply_to_id:
            reply_to = Message.objects.get(pk=reply_to_id)
        else:
            reply_to = None
        new_message = Message.objects.create(
            message=message,
            user=user,
            conversation=conversation,
            reply_to=reply_to
        )
        my_reaction_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_reaction_list"
        )
        other_reactions_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.exclude(user=user).select_related("user").order_by("-created_at")[:3],
            to_attr="other_reactions_list"
        )

        message_with_prefetch = Message.objects.filter(pk=new_message.pk).prefetch_related(
            my_reaction_prefetch,
            other_reactions_prefetch,
        ).select_related("user", "reply_to", "reply_to__user", "shared_post", "shared_post__posted_by").prefetch_related("shared_post__payment_info_list").first()
        serializer = MessageSimpleSerializer(message_with_prefetch)
        
        return Response(serializer.data, status=201)

    @action(detail=False, methods=["get"], permission_classes=[IsActiveConversationMemberForConvBulk])
    def get_bulk(self, request):
        """
        Fetch multiple conversations by comma-separated IDs.
        Example: GET /chat/conversations/get_bulk/?id=1,2,3
        """
        ids = request.query_params.get("id", "")
        if not ids:
            return Response({"error": "No IDs provided"}, status=400)

        try:
            id_list = [int(i) for i in ids.split(",") if i.isdigit()]
        except ValueError:
            return Response({"error": "Invalid ID format"}, status=400)

        if not id_list:
            return Response({"error": "No valid IDs found"}, status=400)

        user = request.user

        # Reuse your existing queryset function
        qs = get_conversation_queryset(user)
        qs = qs.filter(id__in=id_list)

        # Maintain the order of IDs
        conversations_ordered = sorted(qs, key=lambda c: id_list.index(c.id))

        serializer = ConversationSimpleSerializer(conversations_ordered, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsActiveConversationMemberForConvAfterId])
    def latest_conversations(self, request):
        """
        Fetch conversations updated after a given conversation ID.
        Example: GET /chat/conversations/latest_conversations/?after_id=42
        """
        user = request.user
        after_id = request.query_params.get("after_id")
        category = request.query_params.get("category")

        if not after_id:
            return Response({"error": "Missing 'after_id' query parameter"}, status=400)

        try:
            after_id = int(after_id)
        except ValueError:
            return Response({"error": "Invalid 'after_id' format"}, status=400)

        # Get the reference conversation
        try:
            reference_conv = Conversation.objects.get(pk=after_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=404)

        after_time = reference_conv.updated_at

        # Reuse your existing queryset builder
        qs = get_conversation_queryset(user, category).filter(
            updated_at__gt=after_time,
        ).order_by("updated_at")

        serializer = ConversationSimpleSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def chat_with_user(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required"}, status=400)
        try:
            other_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        connection_exists = Connection.objects.filter(
            Q(initiating_user=self.request.user, connected_user=other_user) |
            Q(initiating_user=other_user, connected_user=self.request.user),
            removed=False
        ).exists()
        if not connection_exists:
            return Response({"error": "Connection does not exist"}, status=400)
        existing_conversation = Conversation.objects.filter(members__user=request.user).filter(members__user=other_user).order_by("-updated_at").first()
        print("existing", existing_conversation)
        if existing_conversation:
            existing_conversation_with_details = add_conversation_details(existing_conversation, request.user)
            serializer = ConversationSimpleSerializer(existing_conversation_with_details, many=True)
            return Response(serializer.data)
        conversation = Conversation.objects.create()
        member = Member.objects.create(
            user=request.user,
            conversation=conversation,
            category=ConversationCategoryOptions.PRIMARY
        )
        other_member = Member.objects.create(
            user=other_user,
            conversation=conversation,
            category=ConversationCategoryOptions.REQUESTS
        )
        conversation_with_detail = add_conversation_details(conversation, request.user)

        serializer = ConversationSimpleSerializer(conversation_with_detail, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsActiveConversationMember])
    def archive_conversation_for_me(self, request, pk=None):
        conversation = self.get_object()
        membership = conversation.members.filter(user=request.user)
        membership.update(category=ConversationCategoryOptions.ARCHIVED)
        return Response({"message": "Conversation archived for me"})

    @action(detail=True, methods=['post'], permission_classes=[IsActiveConversationMember])
    def move_conversation(self, request, pk=None):
        category = request.data.get("category")
        if category not in [ConversationCategoryOptions.PRIMARY, ConversationCategoryOptions.SECONDARY]:
            return Response({"error": "Invalid category"}, status=400)
        conversation = self.get_object()
        membership = conversation.members.filter(user=request.user)
        membership.update(category=category)
        return Response({"message": "Conversation moved"})

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def unread_counts(self, request):
        user = request.user
        unread_counts = get_unread_counts_by_category(user)
        return Response(unread_counts)

    @action(detail=True, methods=['post'], permission_classes=[IsActiveConversationMember])
    def share_post(self, request, pk=None):
        post_id = request.data.get("post_id")
        if not post_id:
            return Response({"error": "Post ID is required"}, status=400)
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
        conversation = self.get_object()
        conversation.updated_at = timezone.now()
        conversation.save()
        user = request.user

        post.forwards += 1
        post.save()

        new_message = Message.objects.create(
            shared_post=post,
            user=user,
            conversation=conversation,
        )
        my_reaction_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_reaction_list"
        )
        other_reactions_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.exclude(user=user).select_related("user").order_by("-created_at")[:3],
            to_attr="other_reactions_list"
        )

        message_with_prefetch = Message.objects.filter(pk=new_message.pk).prefetch_related(
            my_reaction_prefetch,
            other_reactions_prefetch,
        ).select_related("shared_post", "shared_post__posted_by").prefetch_related("shared_post__payment_info_list").first()
        serializer = MessageSimpleSerializer(message_with_prefetch)
        
        return Response(serializer.data, status=201)




class MessageViewSet(viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSimpleSerializer
    
    @action(detail=True, methods=["post"], permission_classes=[IsActiveConversationMemberForMessage])
    def react(self, request, pk=None):
        message = self.get_object()
        user = request.user
        emoji = request.data.get("emoji")
        if not emoji:
            return Response({"error": "Emoji is required"}, status=400)
        existing_reaction = Reaction.objects.filter(message=message, user=user).first()
        if existing_reaction:
            existing_reaction.reaction = emoji
            existing_reaction.save()
        else:
            Reaction.objects.create(
                message=message,
                user=user,
                reaction=emoji
            )
        my_reaction_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_reaction_list"
        )
        other_reactions_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.exclude(user=user).select_related("user").order_by("-created_at")[:3],
            to_attr="other_reactions_list"
        )

        message_with_prefetch = Message.objects.filter(pk=message.pk).prefetch_related(
            my_reaction_prefetch,
            other_reactions_prefetch,
        ).select_related("shared_post", "shared_post__posted_by").prefetch_related("shared_post__payment_info_list").first()
        serializer = MessageSimpleSerializer(message_with_prefetch)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsActiveConversationMemberForMessageBulk])
    def get_bulk(self, request):
        """
        Fetch multiple messages by comma-separated IDs.
        Example: GET /chat/messages/get_bulk/?id=1,2,3
        """
        ids = request.query_params.get("id", "")
        print("ids", ids)
        if not ids:
            return Response({"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            id_list = [int(i) for i in ids.split(",") if i.isdigit()]
        except ValueError:
            return Response({"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST)

        if not id_list:
            return Response({"error": "No valid IDs found"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        my_reaction_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_reaction_list"
        )
        other_reactions_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.exclude(user=user).select_related("user").order_by("-created_at")[:3],
            to_attr="other_reactions_list"
        )

        messages_qs = Message.objects.filter(pk__in=id_list).prefetch_related(
            my_reaction_prefetch,
            other_reactions_prefetch,
        ).select_related("user", "reply_to", "reply_to__user", "shared_post", "shared_post__posted_by").prefetch_related("shared_post__payment_info_list")

        existing = set(
            MessageView.objects.filter(user=user, message__in=messages_qs)
            .values_list("message_id", flat=True)
        )
        to_create = [
            MessageView(message=m, user=user)
            for m in messages_qs
            if m.id not in existing
        ]
        if to_create:
            MessageView.objects.bulk_create(to_create)

            message_view_counts = MessageView.objects.filter(
                message_id=OuterRef('id')
            ).values('message_id').annotate(
                count=Count('id')
            ).values('count')

            messages_qs.exclude(id__in=existing).update(
                view_count=Coalesce(
                    Subquery(message_view_counts),
                    Value(0)
                )
            )

        
        # Maintain the order of IDs
        messages_ordered = sorted(messages_qs, key=lambda m: id_list.index(m.id))
        serializer = MessageSimpleSerializer(messages_ordered, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsActiveConversationMemberForMessage])
    def forward(self, request, pk=None):
        message = self.get_object()
        user = request.user
        if message.forwarded_from:
            original_message = message.forwarded_from
        else:
            original_message = message
        new_forward = Message.objects.create(
            forwarded_from=original_message,
            user=user,
            conversation=message.conversation
        )
        my_reaction_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_reaction_list"
        )
        other_reactions_prefetch = Prefetch(
            "reaction_set",
            queryset=Reaction.objects.exclude(user=user).select_related("user").order_by("-created_at")[:3],
            to_attr="other_reactions_list"
        )

        new_forward_with_prefetch = Message.objects.filter(pk=new_forward.pk).prefetch_related(
            my_reaction_prefetch,
            other_reactions_prefetch,
            "reply_to",
            "forwarded_from",
            "forwarded_from__user"
        ).first()
        serializer = MessageSimpleSerializer(new_forward_with_prefetch)
        return Response(serializer.data)
