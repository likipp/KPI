from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == self.request.user or self.request.user.is_superuser


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class CanPutAndUpdate(permissions.DjangoObjectPermissions):

    def has_object_permission(self, request, view, obj):
        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user
        print(view.get_queryset(), 66, request.method)
        if user.has_perm('add_groupkpi', obj):
            # user.
            # self.perms_map = {
            #     'GET': ['kpi.view_groupkpi'],
            #     'POST': ['kpi.add_groupkpi']
            # }
            return True


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
