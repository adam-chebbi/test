from rest_framework.permissions import BasePermission
from authentication.models import Profile

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profileName.name == "SUPER-ADMIN"

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profileName.name in ["SUPER-ADMIN", "ADMIN"]

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profileName.name in ["SUPER-ADMIN", "ADMIN", "MODERATOR"]

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profileName.name in ["SUPER-ADMIN", "ADMIN", "MODERATOR", "USER"]

class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated or (request.user.is_authenticated and request.user.profileName.name == "GUEST")