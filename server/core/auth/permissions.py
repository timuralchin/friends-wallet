from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """Allows access only to authenticated not admin users."""

    def has_permission(self, request, view):
        """If user is usual."""
        user = request.user
        return bool(
            user and
            user.is_authenticated and
            not (user.is_staff or user.is_superuser),
        )
