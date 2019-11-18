from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Menu
from ..serializers.menu_serializer import MenuSerializer
from utils.baseviews import TreeAPIView
from utils.pagination import BasePagination


class MenuViewSet(ModelViewSet, TreeAPIView):
    perms_map = ({'*': 'admin'}, {'*': 'all'}, {'get': 'list'}, {'post': 'create'}, {'put': 'edit'},
                 {'delete': 'delete'})
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = BasePagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('sort',)


class MenuTreeView(TreeAPIView):
    queryset = Menu.objects.all()
