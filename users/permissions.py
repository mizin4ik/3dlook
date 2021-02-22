from rest_framework.permissions import IsAdminUser


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        """Check if a user is the superuser."""
        return bool(request.user and request.user.is_superuser)
