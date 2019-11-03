from rest_framework import serializers
from ..models import Role


class RoleSerializer(serializers.ModelSerializer):
    """
    角色序列化
    """
    class Meta:
        model = Role
        fields = '__all__'
