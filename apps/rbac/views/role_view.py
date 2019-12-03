from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Role
from ..serializers.role_serializer import RoleListSerializer, RoleModifySerializer, PermissionTableSerializer
from ..serializers.menu_serializer import MenuSerializer
from .permission_view import PermissionToMenuView
from utils.baseviews import RoleBaseView
from utils.pagination import BasePagination


class RoleViewSet(ModelViewSet):
    """
    角色管理: 增删改查
    """
    queryset = Role.objects.all()
    pagination_class = BasePagination
    serializer_class = RoleListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)

    # def get_serializer_class(self):
    #     #     if self.action == 'list':
    #     #         return RoleListSerializer
    #     #     return RoleModifySerializer


class RoleTreeViewSet(RoleBaseView):
    queryset = Role.objects.all()
    serializer_class = RoleModifySerializer
