from rest_framework import serializers

from ..models import Permission
from utils.baseviews import TreeSerializer


class PermissionListSerializer(serializers.ModelSerializer):
    """
    权限列表序列化
    """
    # menuname = serializers.ReadOnlyField(source='menus.name')

    class Meta:
        model = Permission
        # fields = ('id', 'name', 'method', 'menuname', 'pid')
        fields = '__all__'


class PermissionToRoleSerializer(TreeSerializer, serializers.ModelSerializer):
    permission_type_choices = (
        ("children", "子级"),
        ("parent", "父级")
    )
    type = serializers.ChoiceField(choices=permission_type_choices, source="get_type_display", default='children')

    class Meta:
        model = Permission
        fields = ('id', 'name', 'pid', 'method', 'type')
