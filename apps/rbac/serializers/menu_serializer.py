from rest_framework import serializers
from ..models import Menu


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单序列化
    """
    # 因为使用iconFont在iView中需要加空格,到后端会删除空格.所以需要设置trim_whitespace=False.官方资料中有介绍
    icon = serializers.CharField(max_length=50, allow_blank=True, allow_null=True, trim_whitespace=False)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'icon', 'path', 'is_show','is_frame', 'sort', 'component', 'pid')
        extra_kwargs = {'name': {'required': True, 'error_messages': {'required': '必须填写菜单名'}}}

