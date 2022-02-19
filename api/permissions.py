from rest_framework.permissions import BasePermission


class IsNora(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(request.user.is_authenticated and request.user.username == "nora")

    def has_object_permission(self, request, view, obj) -> bool:
        return bool(request.user.is_authenticated and request.user.username == "nora")
