from collections import OrderedDict

from rest_framework import serializers

from ..models import Role, Permission
from utils.baseviews import PermissionTableSerializer, TreeSerializer
from ..serializers.menu_serializer import MenuSerializer


class RoleListSerializer(serializers.ModelSerializer):
    """
    角色序列化
    """
    # permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Role
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(RoleListSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            member_set = instance.userProfile_roles.all()
            members = [{'id': user.id, 'name': user.name, 'username': user.username} for user in member_set]
            ret['members'] = members
            # ret['permissions'] = serializer_permissions.data
            return ret


class RoleModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(RoleModifySerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            serializer_permissions = PermissionTableSerializer(data=instance.permissions.all(), many=True)
            serializer_menus = MenuSerializer(data=instance.menus.all(), many=True)
            serializer_permissions.is_valid()
            serializer_menus.is_valid()
            member_set = instance.userProfile_roles.all()
            members = [{'id': user.id, 'name': user.name, 'username': user.username} for user in member_set]
            ret['members'] = members
            ret['permissions'] = serializer_permissions.data
            ret['menus'] = serializer_menus.data
            return ret
