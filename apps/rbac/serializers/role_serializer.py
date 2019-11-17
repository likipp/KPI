from collections import OrderedDict

from rest_framework import serializers

from ..models import Role


class RoleListSerializer(serializers.ModelSerializer):
    """
    角色序列化
    """
    class Meta:
        model = Role
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(RoleListSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            member_set = instance.userProfile_roles.all()
            members = [{'id': user.id, 'name': user.name, 'username': user.username} for user in member_set]
            ret['members'] = members
            return ret


class RoleModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
