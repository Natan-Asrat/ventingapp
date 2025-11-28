from rest_framework import permissions

class IsReportAboutOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow the report to be accessed by who it is about, who reported it or a staff member.
    """

    def has_object_permission(self, request, view, obj):
        # obj here is the Post instance
        is_about_user = obj.report.about_user == request.user
        is_reported_by_user = obj.report.reported_by == request.user
        return is_about_user or is_reported_by_user or request.user.is_staff
