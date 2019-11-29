from rest_framework import serializers
from ..models import UserProfile
import re


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表序列化
    """
    # roles = serializers.SerializerMethodField()
    # superior = serializers.SerializerMethodField()
    # position = serializers.SerializerMethodField()
    # department = serializers.SerializerMethodField()
    #
    # def get_roles(self, obj):
    #     return obj.roles.values()
    #
    # def get_superior(self, obj):
    #     if obj.superior is not None:
    #         superior = {
    #             "id": obj.superior.id,
    #             "name": obj.superior.name
    #         }
    #         return superior
    #     else:
    #         superior = {}
    #         return superior
    #
    # def get_position(self, obj):
    #     if obj.position is not None:
    #         position = {
    #             "id": obj.position.id,
    #             "name": obj.position.name
    #         }
    #         return position
    #     else:
    #         position = {}
    #         return position
    #
    # def get_department(self, obj):
    #     if obj.department is not None:
    #         department = {
    #             "id": obj.department.id,
    #             "name": obj.department.name
    #         }
    #         return department
    #     else:
    #         department = {}
    #         return department

    def to_representation(self, instance):
        ret = super(UserListSerializer, self).to_representation(instance)
        if instance.superior is not None:
            ret['superior'] = {'id': instance.superior.id, 'name': instance.superior.name}
        else:
            ret['superior'] = {}
        if instance.department is not None:
            ret['department'] = {'id': instance.department.id, 'name': instance.department.name}
        else:
            ret['department'] = {}
        if instance.position is not None:
            ret['position'] = {'id': instance.position.id, 'name': instance.position.name}
        else:
            ret['position'] = {}
        return ret

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'avatar', 'department', 'position', 'superior',
                  "is_superuser", "is_staff",  'is_active', 'roles']
        # depth = 1


class UserModifySerializer(serializers.ModelSerializer):
    """
    用户编辑的序列化
    """
    mobile = serializers.CharField(max_length=11, label="手机号码")

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'department', 'position', 'superior',
                  'is_active', 'roles', 'avatar']

    def validate_mobile(self, mobile):
        regex_mobile = "^1[358]\\d{9}$|^147\\d{8}$|^176\\d{8}$"
        if not re.match(regex_mobile, mobile):
            raise serializers.ValidationError("手机号码不合法")
        return mobile


class UserCreateSerializer(serializers.ModelSerializer):
    """
    创建用户序列化
    """
    username = serializers.CharField(required=True, allow_blank=False, label="账号")
    mobile = serializers.CharField(max_length=11, label="手机号码")

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'department',
                  'position', 'is_active', 'roles', 'superior']

    def validate_username(self, username):
        if UserProfile.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_mobile(self, mobile):
        regex_mobile = "^1[358]\\d{9}$|^147\\d{8}$|^176\\d{8}$"
        if not re.match(regex_mobile, mobile):
            raise serializers.ValidationError("手机号码不合法")
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError("手机号已经被注册")
        return mobile

    def create(self, validated_data):
        instance = super(UserCreateSerializer, self).create(validated_data)
        instance.set_password('123456')
        instance.save()
        return instance


class UserInfoListSerializer(serializers.ModelSerializer):
    """
    公共users
    """
    department = serializers.SerializerMethodField()

    def get_department(self, obj):
        if obj.department is not None:
            department = {
                "id": obj.department.id,
                "name": obj.department.name
            }
            return department
        else:
            department = {}
            return department

    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'mobile', 'email', 'position', 'username',
                  "is_superuser", "is_staff", "is_active", "department", "superior")
