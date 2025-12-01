from rest_framework import viewsets, mixins
from .models import Conversation, Member, Message, Reaction, ConversationCategoryOptions
from .serializers import ConversationSimpleSerializer, MessageSimpleSerializer
from django.db.models import Prefetch
from rest_framework.decorators import action
from rest_framework.response import Response 
from .permissions import IsActiveConversationMember, IsActiveConversationMemberForMessage

# Create your views here.
class ConversationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Conversation.objects.none()
    serializer_class = ConversationSimpleSerializer
    def get_queryset(self):
        user = self.request.user
        category = self.request.query_params.get("category")

        my_membership_prefetch = Prefetch(
            "members",
            queryset=Member.objects.filter(user=user).order_by("-created_at"),
            to_attr="my_membership_list"
        )
        other_user_prefetch = Prefetch(
            "members",
            queryset=Member.objects.exclude(user=user).select_related("user")[:3],
            to_attr="other_user_list"
        )

        qs = Conversation.objects.filter(
            active=True,
            members__user=user
        )

        if category:
            qs = qs.filter(
                members__user=user,
                members__category=category
            )

        qs = qs.prefetch_related(my_membership_prefetch, other_user_prefetch).distinct()

        return qs

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
            "reply_to"
        ).select_related("user", "reply_to", "reply_to__user").order_by("-created_at")

        serializer = MessageSimpleSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsActiveConversationMember])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
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
            "reply_to"
        ).first()
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
            "reply_to"
        ).first()
        serializer = MessageSimpleSerializer(message_with_prefetch)
        return Response(serializer.data)