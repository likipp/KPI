from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from ..models import Permission
from ..serializers.permission_serializer import PermissionListSerializer
from utils.baseviews import TreeAPIView


class PermissionViewSet(viewsets.ModelViewSet, TreeAPIView):
    """
    权限: 增删改查
    """
    perms_map = ({'*': 'admin'}, {'*': 'permission_all'}, {'get': 'permission_list'}, {'post': 'permission_create'},
                 {'put': 'permission_edit'}, {'delete': 'permission_delete'})
    queryset = Permission.objects.all()
    serializer_class = PermissionListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)


class PermissionTreeView(TreeAPIView):
    queryset = Permission.objects.all()
