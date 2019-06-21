from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnlyCustom(BasePermission):

    def has_permission(self, request, view):
        return request.method.lower() == 'get' or request.user.is_authenticated or (
                request.method.lower() == 'post' or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.method.lower() == 'get' or request.user.is_authenticated or (
                request.method.lower() in ['delete', 'put'] or request.user.is_authenticated)

class PermissionMovieRate():
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )