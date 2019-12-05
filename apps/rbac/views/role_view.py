from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from ..models import Role
from ..serializers.role_serializer import RoleListSerializer, RoleModifySerializer, RoleSingleUpdateSerializer
from ..serializers.permission_serializer import PermissionToRoleSerializer
from ..serializers.menu_serializer import MenuSerializer
from .permission_view import PermissionToMenuView
from utils.baseviews import RoleBaseView
from utils.pagination import BasePagination


class RoleViewSet(ModelViewSet, RoleBaseView):
    """
    角色管理: 增删改查
    """
    queryset = Role.objects.all()
    pagination_class = BasePagination
    serializer_class = RoleListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)

    @action(detail=True, methods=['patch'], url_path='delete-role-permission', url_name='delete-role-permission')
    # 获取后端提供过来的角色ID(pk), 权限ID(request.data['permission) PATCH方法
    def delete_permission_from_role(self, request, pk=None):
        role = Role.objects.filter(id=pk).first()
        print(role, request.data['id'])
        for i in role.permissions.all():
            if i.id == int(request.data['id']):
                role.permissions.remove(i)
        permission = RoleSingleUpdateSerializer(many=True, data=Role.objects.all())
        permission.is_valid()
        print(permission.data)
        return Response(permission.data)

    # @action(detail=True, methods=['get'], url_path='get-role-permission', url_name='get-role-permission')
    # def get_permissions_from_role(self, request, pk=None):
    #     return Response(2222)

    # def get_serializer_class(self):
    #     #     if self.action == 'list':
    #     #         return RoleListSerializer
    #     #     return RoleModifySerializer


class RoleTreeViewSet(RoleBaseView):
    queryset = Role.objects.all()
    serializer_class = RoleModifySerializer


class RoleSingleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSingleUpdateSerializer

    @action(detail=True, methods=['get'], url_path='get-single-role', url_name='et-single-role')
    def get_role(self, request, pk=None):
        return Response(2222)
