from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_role


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin_role
            or (request.user.is_staff_role and request.user.verified)
        )


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient


class IsStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin_role
            or (request.user.is_staff_role and request.user.verified)
        )


class IsOwnPatientData(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_patient:
            return obj.user == request.user
        return True