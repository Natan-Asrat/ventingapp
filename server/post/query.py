
from .models import Like, Save
from django.db.models import Exists, OuterRef, Q
from account.models import Connection

def get_posts_queryset(post_qs, user):
    return post_qs.annotate(
            liked=Exists(Like.objects.filter(post=OuterRef("pk"), liked_by=user, active=True)),
            saved=Exists(Save.objects.filter(post=OuterRef("pk"), saved_by=user, active=True)),
            connected=Exists(Connection.objects.filter(
                Q(initiating_user=user, connected_user=OuterRef("posted_by")) |
                Q(initiating_user=OuterRef("posted_by"), connected_user=user),
                removed=False
            )),
            pending_connection=Exists(Connection.objects.filter(
                Q(initiating_user=user, connected_user=OuterRef("posted_by")) |
                Q(initiating_user=OuterRef("posted_by"), connected_user=user),
                reconnection_requested=True,
                removed=True,
                reconnection_rejected=False
            )),
            rejected_connection=Exists(Connection.objects.filter(
                Q(initiating_user=user, connected_user=OuterRef("posted_by")) |
                Q(initiating_user=OuterRef("posted_by"), connected_user=user),
                removed=True,
                reconnection_rejected=True
            )),
            banned_connection=Exists(Connection.objects.filter(
                Q(initiating_user=user, connected_user=OuterRef("posted_by")) |
                Q(initiating_user=OuterRef("posted_by"), connected_user=user),
                banned=True
            )),
            removed_connection=Exists(Connection.objects.filter(
                Q(initiating_user=user, connected_user=OuterRef("posted_by")) |
                Q(initiating_user=OuterRef("posted_by"), connected_user=user),
                removed=True,
            )),
        )