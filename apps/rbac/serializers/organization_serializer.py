from rest_framework import serializers
from ..models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    组织结构序列化
    """

    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')


class OrganizationUserTreeSerializer(serializers.ModelSerializer):
    """
    组织结构树序列化
    """
    # title = serializers.CharField(max_length=20, source='name')
    # organization_type_choices = (
    #     ("company", "公司"),
    #     ("department", "部门")
    # )
    # type = serializers.ChoiceField(choices=organization_type_choices, source="get_type_display")
    label = serializers.StringRelatedField(source='name')
    children = UserSerializer(many=True, read_only=True, source='userprofile_set')

    class Meta:
        model = Organization
        fields = ('id', 'label', 'pid', 'children')
