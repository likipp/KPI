from collections import OrderedDict

from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.response import Response

from rbac.models import Menu, Permission
from rbac.serializers.menu_serializer import MenuSerializer


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


class RoleBaseView(ListAPIView):
    serializer_class = PermissionTableSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        # tree_data = []
        role_list = []
        for item in serializer.data:
            tree_dict[item['id']] = item

        # print(tree_dict, 66666)
        for i in queryset:
            role_dict = OrderedDict()
            role_dict['id'] = i.id
            role_dict['name'] = i.name
            role_dict['members'] = [{'id': user.id,
                                    'name': user.name,
                                     'username': user.username} for user in i.userProfile_roles.all()]
            serializer_menu = TreeSerializer(i.menus.all(), many=True)
            menu_dict = {}
            button_dict = {}
            tree_data = []
            for item in serializer_menu.data:
                button_dict[item['id']] = item
            menu_dict.setdefault(i.id, []).append(button_dict)

            for x in menu_dict:
                for y in menu_dict[x]:
                    for z in y:
                        if y[z]['pid']:
                            pid = y[z]['pid']
                            parent = y[pid]
                            parent.setdefault('children', []).append(y[z])
                            for a in tree_dict:
                                if a == x:
                                    for b in tree_dict[a]['permissions']:
                                        if y[z]['id'] == b['pid']:
                                            b['type'] = 'children'
                                            y[z].setdefault('children', []).append(b)
                        else:
                            tree_data.append(y[z])
            role_dict['permissions'] = tree_data
            role_list.append(role_dict)
        return Response(role_list)

