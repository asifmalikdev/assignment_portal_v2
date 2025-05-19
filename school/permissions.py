from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowPostForAnon(BasePermission):
    def has_permission(self, request, view):
        # Allow POST even if user is anonymous
        if request.method == 'POST':
            return True
        # For all other methods, require authentication
        return request.user and request.user.is_authenticated
