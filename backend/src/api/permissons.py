from rest_framework.permissions import (
    BasePermission,
    IsAdminUser,

    )  

class IsAdminAuthentication(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user.is_admin)

class IsStaffAuthentication(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user.is_staff)