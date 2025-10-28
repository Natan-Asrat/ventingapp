from rest_framework import permissions

class IsPostOwner(permissions.BasePermission):
    """
    Custom permission to only allow the post owner to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        # obj here is the Post instance
        return obj.posted_by == request.user
