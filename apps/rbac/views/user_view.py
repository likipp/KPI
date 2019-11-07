from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
import django_filters

from ..models import UserProfile
from ..filters import UserFilter
from utils.baseviews import BasePagination
from ..serializers.user_serializer import UserListSerializer, UserCreateSerializer, UserModifySerializer, UserInfoListSerializer


class UserInfoView(APIView):

    def get(self, request):
        user = request.user
        print(user, 2222)
        if user is not None:
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
                'create_time': user.date_joined
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

    # def create(self, request, *args, **kwargs):
    #     copy_data = request.data.copy()
    #     copy_data['password'] = '123456'
    #     serializer = self.get_serializer(data=copy_data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data)
    
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
