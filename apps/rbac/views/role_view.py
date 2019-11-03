from rest_framework.viewsets import ViewSet
from ..models import Role
from ..serializers.role_serializer import RoleSerializer
from rest_framework.filters import SearchFilter, OrderingFilter


class RoleViewSet(ViewSet):
    """
    角色管理: 增删改查
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.action == 'list':
            return RoleSerializer
