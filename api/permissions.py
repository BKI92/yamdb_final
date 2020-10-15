from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(
                request.user.role == 'admin' or request.user.is_superuser)


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(
                request.user.role == 'admin' or request.user.is_superuser)


class IsModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.role == 'moderator')


class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsStaffOrAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.method in ('PATH', 'DELETE'):
                return (obj.author == request.user or request.user.role in (
                    'admin', 'moderator') or request.user.is_superuser)
            return (obj.author == request.user or request.user.role in (
                'admin', 'moderator') or request.user.is_superuser)

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True
