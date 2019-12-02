from collections import OrderedDict

from rest_framework import serializers

from ..models import Role


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
            print(instance.permissions.all(), 6666)
            # ret['menus'] = [{'id': menu.id, 'name': menu.name} for menu in instance.menus.all()]
            # ret['permissions'] = [{'id': permission.id, 'name': permission.name}
            #                       for permission in instance.permissions.all()]
            member_set = instance.userProfile_roles.all()
            members = [{'id': user.id, 'name': user.name, 'username': user.username} for user in member_set]
            ret['members'] = members
            return ret


class RoleModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
