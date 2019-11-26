from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from ..models import Permission
from ..serializers.permission_serializer import PermissionListSerializer
from utils.baseviews import TreeAPIView, PermissionToMenuView


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限: 增删改查
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)


class PermissionTreeView(PermissionToMenuView):
    queryset = Permission.objects.all()
