from rest_framework import permissions
from .models import Connection

class IsConnectedUser(permissions.BasePermission):
    """
    Custom permission to only allow the report to be accessed by who it is about, who reported it or a staff member.
    """
    def has_permission(self, request, view):
        connection_id = request.data.get('connection_id')
        if not connection_id:
            return False
        try:
            connection = Connection.objects.get(id=connection_id)
        except Connection.DoesNotExist:
            return False
        return connection.connected_user == request.user