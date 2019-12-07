from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == self.request.user or self.request.user.is_superuser


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.METHOD == 'GET':
            return self.request.user.is_superuser
        else:
            return True
