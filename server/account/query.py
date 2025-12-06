from .models import User, Connection
from django.db.models import Q, Count, Exists, OuterRef


def annotate_user_qs(qs, current_user):
    base_filter = (
        Q(initiating_user=current_user, connected_user=OuterRef("pk")) |
        Q(initiating_user=OuterRef("pk"), connected_user=current_user)
    )
    return qs.annotate(
        connected=Exists(
            Connection.objects.filter(base_filter, removed=False)
        ),
        pending_connection=Exists(
            Connection.objects.filter(
                base_filter,
                removed=True,
                reconnection_requested=True,
                reconnection_rejected=False
            )
        ),
        rejected_connection=Exists(
            Connection.objects.filter(
                base_filter,
                removed=True,
                reconnection_rejected=True
            )
        ),
        banned_connection=Exists(
            Connection.objects.filter(base_filter, banned=True)
        ),
        removed_connection=Exists(
            Connection.objects.filter(base_filter, removed=True)
        ),
        followers=Count(
            "connected_users",
            filter=Q(connected_users__removed=False),
            distinct=True
        )
    )
def get_other_profile_queryset(user_id, current_user):
    qs = User.objects.filter(id=user_id)
    qs = annotate_user_qs(qs, current_user)

    annotated_user = qs.first()
    return annotated_user