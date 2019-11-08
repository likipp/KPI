from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Menu
from ..serializers.menu_serializer import MenuSerializer
from utils.baseviews import BasePagination, TreeAPIView


class MenuViewSet(ModelViewSet, TreeAPIView):
    perms_map = ({'*': 'admin'}, {'*': 'menu_all'}, {'get': 'menu_list'}, {'post': 'menu_create'}, {'put': 'menu_edit'},
                 {'delete': 'menu_delete'})
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = BasePagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('sort',)


class MenuTreeView(TreeAPIView):
    queryset = Menu.objects.all()
