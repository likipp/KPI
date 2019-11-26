from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.response import Response

from rbac.models import Menu, Permission


class TreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)


class PermissionTableSerializer(TreeSerializer, serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('id', 'name', 'pid', 'method')


class TreeAPIView(ListAPIView):
    serializer_class = TreeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)


class PermissionBaseView(ListAPIView):
    serializer_class = PermissionTableSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        serializer_menu = self.get_serializer(Menu.objects.all(), many=True)
        tree_dict = {}
        menu_dict = {}
        tree_data = []
        menu_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for item in serializer_menu.data:
                menu_dict[item['id']] = item
            for i in menu_dict:
                if menu_dict[i]['pid']:
                    pid = menu_dict[i]['pid']
                    parent = menu_dict[pid]
                    parent.setdefault('children', []).append(menu_dict[i])
                    for y in tree_dict:
                        if menu_dict[i]['id'] == tree_dict[y]['pid']:
                            tree_dict[y]['type'] = 'children'
                            menu_dict[i].setdefault('children', []).append(tree_dict[y])
                            menu_data.append(menu_dict[i])
                else:
                    tree_data.append(menu_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)
