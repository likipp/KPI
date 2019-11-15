from operator import itemgetter

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ..models import UserProfile, Menu
from ..filters import UserFilter
from utils.baseviews import BasePagination
from ..serializers.user_serializer import UserListSerializer, UserCreateSerializer, UserModifySerializer
from ..serializers.menu_serializer import MenuSerializer


class UserInfoView(APIView):

    @classmethod
    def get_permission_from_role(self, request):
        try:
            if request.user:
                perms_list = []
                for item in request.user.roles.values('permissions__method').distinct():
                    perms_list.append(item['permissions__method'])
                return perms_list
        except AttributeError:
            return None
    # 定义用户所属的roles组

    def get_roles(self, request):
        try:
            if request.user:
                role = []
                if request.user.roles:
                    for item in request.user.roles.all():
                        role.append(item.name)
                        return role
        except AttributeError:
            return None

    def get_menu_from_role(self, request):
        if request.user:
            menu_dict = {}
            menus = request.user.roles.values(
                'menus__id',
                'menus__name',
                'menus__path',
                'menus__is_frame',
                'menus__is_show',
                'menus__component',
                'menus__icon',
                'menus__sort',
                'menus__pid'
            ).distinct()
            for item in menus:
                if item['menus__pid'] is None:
                    if item['menus__is_frame']:
                        # 判断是否外部链接
                        top_menu = {
                            'id': item['menus__id'],
                            'path': item['menus__path'],
                            'component': 'components/main',
                            'children': [{
                                'path': item['menus__path'],
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon']
                                }
                            }],
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        top_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': '/' + item['menus__path'],
                            'component': 'components/main',
                            'alwaysShow': True,
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon']
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'children': []
                        }
                    menu_dict[item['menus__id']] = top_menu
                else:
                    if item['menus__is_frame']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': 'components/main',
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'permType': self.get_permission_from_role(request)
                        }
                    elif item['menus__is_show']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'permType': self.get_permission_from_role(request)
                        }
                    else:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'noCache': True,
                            },
                            'hidden': True,
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'permType': self.get_permission_from_role(request)
                        }
                    menu_dict[item['menus__id']] = children_menu
            return menu_dict

    def get_all_menu_dict(self):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        tree_dict = {}
        for item in serializer.data:
            if item['pid'] is None:
                if item['is_frame']:
                    # 判断是否外部链接
                    top_menu = {
                        'id': item['id'],
                        'path': item['path'],
                        'component': 'components/main',
                        'children': [{
                            'path': item['path'],
                            'meta': {
                                'title': item['name'],
                                'icon': item['icon']
                            }
                        }],
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    top_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': '/' + item['path'],
                        'component': 'components/main',
                        'alwaysShow': True,
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon']
                        },
                        'pid': item['pid'],
                        'sort': item['sort'],
                        'children': []
                    }
                tree_dict[item['id']] = top_menu
            else:
                if item['is_frame']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': 'components/main',
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                elif item['is_show']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'noCache': True,
                        },
                        'hidden': True,
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                tree_dict[item['id']] = children_menu
        return tree_dict

    def get_all_menus(self, request):
        perms = UserInfoView.get_permission_from_role(request)
        tree_data = []
        if 'admin' in perms or request.user.is_superuser:
            tree_dict = self.get_all_menu_dict()
        else:
            tree_dict = self.get_menu_from_role(request)
        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                parent = tree_dict[pid]
                parent.setdefault('alwaysShow', True)
                parent.setdefault('children', []).append(tree_dict[i])
                # parent['children'] = sorted(parent['children'], key=itemgetter('sort'))
            else:
                tree_data.append(tree_dict[i])
        return tree_data

    def get(self, request):
        user = request.user
        if user is not None:
            # perms = self.get_permission_from_role(request)
            roles = self.get_roles(request)
            routerData = self.get_all_menus(request)
            data = {
                'id': user.id,
                'username': user.username,
                # request.build_absolute_uri(), 获取到http://127.0.0.1:8000/api/users/info
                # user.avatar提示'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
                # current_scheme_host是Django HttpRequest类中内置的一个方法
                # _request_current_scheme_host是一个受保护的类,所以调用会有警告
                'avatar': request._request._current_scheme_host + '/media/' + str(request.user.avatar),
                'email': user.email,
                'is_active': user.is_active,
                'create_time': user.date_joined,
                # 'roles': perms,
                'roles': roles,
                'routerData': routerData
            }
            return Response(data)


class UserViewSet(ModelViewSet):
    """
        retrieve:
                返回指定用户信息
        update:
                更新用户信息
        destroy:
                删除用户记录
        create:
                创建用户记录
        partial_update:
                更新记录部分字段
        """
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('is_active',)
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        else:
            return UserModifySerializer

    def set_password(self, request, pk=None):
        user = UserProfile.objects.filter(id=pk)
        new_password1 = request.data['new_password1']
        new_password2 = request.data['new_password2']
        if new_password1 == new_password2:
            user.set_password(new_password2)
            return Response('密码修改成功')
        else:
            return Response('密码修改失败，两次输入不一致')


class UserListView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    filter_class = UserFilter
    # filter_backends = (filters.SearchFilter,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    ordering_fields = ('id', 'date_joined',)
    search_fields = ['username', 'name', 'department__name']


# class UserBuildMenuView(APIView):
#
#     def get_menu_from_role(self, request):
#         if request.user:
#             menu_dict = {}
#             menus = request.user.roles.values(
#                 'menus__id',
#                 'menus__name',
#                 'menus__path',
#                 'menus__is_frame',
#                 'menus__is_show',
#                 'menus__component',
#                 'menus__icon',
#                 'menus__sort',
#                 'menus__pid'
#             ).distinct()
#             for item in menus:
#                 if item['menus__pid'] is None:
#                     if item['menus__is_frame']:
#                         # 判断是否外部链接
#                         top_menu = {
#                             'id': item['menus__id'],
#                             'path': item['menus__path'],
#                             'component': 'components/main',
#                             'children': [{
#                                 'path': item['menus__path'],
#                                 'meta': {
#                                     'title': item['menus__name'],
#                                     'icon': item['menus__icon']
#                                 }
#                             }],
#                             'pid': item['menus__pid'],
#                             'sort': item['menus__sort']
#                         }
#                     else:
#                         top_menu = {
#                             'id': item['menus__id'],
#                             'name': item['menus__name'],
#                             'path': '/' + item['menus__path'],
#                             'component': 'components/main',
#                             'alwaysShow': True,
#                             'meta': {
#                                 'title': item['menus__name'],
#                                 'icon': item['menus__icon']
#                             },
#                             'pid': item['menus__pid'],
#                             'sort': item['menus__sort'],
#                             'children': []
#                         }
#                     menu_dict[item['menus__id']] = top_menu
#                 else:
#                     if item['menus__is_frame']:
#                         children_menu = {
#                             'id': item['menus__id'],
#                             'name': item['menus__name'],
#                             'path': item['menus__path'],
#                             'component': 'components/main',
#                             'meta': {
#                                 'title': item['menus__name'],
#                                 'icon': item['menus__icon'],
#                             },
#                             'pid': item['menus__pid'],
#                             'sort': item['menus__sort']
#                         }
#                     elif item['menus__is_show']:
#                         children_menu = {
#                             'id': item['menus__id'],
#                             'name': item['menus__name'],
#                             'path': item['menus__path'],
#                             'component': item['menus__component'],
#                             'meta': {
#                                 'title': item['menus__name'],
#                                 'icon': item['menus__icon'],
#                             },
#                             'pid': item['menus__pid'],
#                             'sort': item['menus__sort']
#                         }
#                     else:
#                         children_menu = {
#                             'id': item['menus__id'],
#                             'name': item['menus__name'],
#                             'path': item['menus__path'],
#                             'component': item['menus__component'],
#                             'meta': {
#                                 'title': item['menus__name'],
#                                 'noCache': True,
#                             },
#                             'hidden': True,
#                             'pid': item['menus__pid'],
#                             'sort': item['menus__sort']
#                         }
#                     menu_dict[item['menus__id']] = children_menu
#             return menu_dict
#
#     def get_all_menu_dict(self):
#         menus = Menu.objects.all()
#         serializer = MenuSerializer(menus, many=True)
#         tree_dict = {}
#         for item in serializer.data:
#             if item['pid'] is None:
#                 if item['is_frame']:
#                     # 判断是否外部链接
#                     top_menu = {
#                         'id': item['id'],
#                         'path': item['path'],
#                         'component': 'components/main',
#                         'children': [{
#                             'path': item['path'],
#                             'meta': {
#                                 'title': item['name'],
#                                 'icon': item['icon']
#                             }
#                         }],
#                         'pid': item['pid'],
#                         'sort': item['sort']
#                     }
#                 else:
#                     top_menu = {
#                         'id': item['id'],
#                         'name': item['name'],
#                         'path': '/' + item['path'],
#                         'component': 'components/main',
#                         'alwaysShow': True,
#                         'meta': {
#                             'title': item['name'],
#                             'icon': item['icon']
#                         },
#                         'pid': item['pid'],
#                         'sort': item['sort'],
#                         'children': []
#                     }
#                 tree_dict[item['id']] = top_menu
#             else:
#                 if item['is_frame']:
#                     children_menu = {
#                         'id': item['id'],
#                         'name': item['name'],
#                         'path': item['path'],
#                         'component': 'components/main',
#                         'meta': {
#                             'title': item['name'],
#                             'icon': item['icon'],
#                         },
#                         'pid': item['pid'],
#                         'sort': item['sort']
#                     }
#                 elif item['is_show']:
#                     children_menu = {
#                         'id': item['id'],
#                         'name': item['name'],
#                         'path': item['path'],
#                         'component': item['component'],
#                         'meta': {
#                             'title': item['name'],
#                             'icon': item['icon'],
#                         },
#                         'pid': item['pid'],
#                         'sort': item['sort']
#                     }
#                 else:
#                     children_menu = {
#                         'id': item['id'],
#                         'name': item['name'],
#                         'path': item['path'],
#                         'component': item['component'],
#                         'meta': {
#                             'title': item['name'],
#                             'noCache': True,
#                         },
#                         'hidden': True,
#                         'pid': item['pid'],
#                         'sort': item['sort']
#                     }
#                 tree_dict[item['id']] = children_menu
#         return tree_dict
#
#     def get_all_menus(self, request):
#         perms = UserInfoView.get_permission_from_role(request)
#         tree_data = []
#         if 'admin' in perms or request.user.is_superuser:
#             tree_dict = self.get_all_menu_dict()
#         else:
#             tree_dict = self.get_menu_from_role(request)
#         for i in tree_dict:
#             if tree_dict[i]['pid']:
#                 pid = tree_dict[i]['pid']
#                 parent = tree_dict[pid]
#                 parent.setdefault('alwaysShow', True)
#                 parent.setdefault('children', []).append(tree_dict[i])
#                 # parent['children'] = sorted(parent['children'], key=itemgetter('sort'))
#             else:
#                 tree_data.append(tree_dict[i])
#         return tree_data
#
#     def get(self, request):
#         if request.user.id is not None:
#             menu_data = self.get_all_menus(request)
#             return Response(menu_data)
#         else:
#             return Response('请登录后访问')
