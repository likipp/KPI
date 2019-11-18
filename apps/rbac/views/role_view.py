from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Role
from ..serializers.role_serializer import RoleListSerializer, RoleModifySerializer
from utils.pagination import BasePagination


class RoleViewSet(ModelViewSet):
    """
    角色管理: 增删改查
    """
    perms_map = ({'*': 'admin'}, {'*': 'role_all'}, {'get': 'role_list'}, {'post': 'role_create'}, {'put': 'role_edit'},
                 {'delete': 'role_delete'})
    queryset = Role.objects.all()
    pagination_class = BasePagination
    serializer_class = RoleListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleListSerializer
        return RoleModifySerializer
