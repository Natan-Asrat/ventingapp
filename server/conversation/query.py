from django.db.models import OuterRef, Subquery, Count, IntegerField, Prefetch, Q
from django.db.models import Case, When, Value, F, Min
from django.db.models.functions import Coalesce, Greatest
from .models import Conversation, Member, Message, MessageView

def get_conversation_queryset(user, category=None):
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

    # Prefetch the latest message
    last_message_prefetch = Prefetch(
        "message_set",
        queryset=Message.objects.order_by("-created_at")[:1],
        to_attr="last_message_list"
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


    latest_view_subquery = MessageView.objects.filter(
        user=user,
        message__conversation=OuterRef('pk')
    ).order_by('-created_at').values('message__created_at')[:1]

    # Count messages after latest view, or all if none
    qs = qs.annotate(
        new_messages_count=Count(
            'message',  # Use the ForeignKey field name, not message_set
            filter=Q(message__created_at__gt=Coalesce(Subquery(latest_view_subquery), Value('1970-01-01'))),
            output_field=IntegerField()
        )
    )


    qs = qs.prefetch_related(my_membership_prefetch, other_user_prefetch, last_message_prefetch).distinct()
    return qs

def add_conversation_details(conversation, user):
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

    # Prefetch the latest message
    last_message_prefetch = Prefetch(
        "message_set",
        queryset=Message.objects.order_by("-created_at")[:1],
        to_attr="last_message_list"
    )


    latest_view_subquery = MessageView.objects.filter(
        user=user,
        message__conversation=OuterRef('pk')
    ).order_by('-created_at').values('message__created_at')[:1]
    qs = Conversation.objects.filter(pk=conversation.pk)

    # Count messages after latest view, or all if none
    qs = qs.annotate(
        new_messages_count=Count(
            'message',  # Use the ForeignKey field name, not message_set
            filter=Q(message__created_at__gt=Coalesce(Subquery(latest_view_subquery), Value('1970-01-01'))),
            output_field=IntegerField()
        )
    )


    qs = qs.prefetch_related(my_membership_prefetch, other_user_prefetch, last_message_prefetch)
    return qs