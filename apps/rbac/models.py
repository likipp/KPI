from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Menu(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    path = models.CharField(max_length=158, null=True, blank=True, verbose_name="链接地址")
    is_frame = models.BooleanField(default=False, verbose_name="外部菜单")
    is_show = models.BooleanField(default=True, verbose_name="显示标记")
    sort = models.IntegerField(null=True, blank=True, verbose_name="排序标记")
    component = models.CharField(max_length=200, null=True, blank=True, verbose_name="组件")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")
    # roles = GenericRelation(to="Role")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="权限名")
    method = models.CharField(max_length=50, null=True, blank=True, verbose_name="方法")
    pid = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.PROTECT, verbose_name='父级菜单')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']


# class Permissions(models.Model):
#     """
#     权限
#     """
#     permission_type_choices = (
#         ("menu", "菜单"),
#         ("button", "按钮")
#     )
#     name = models.CharField(max_length=30, unique=True, verbose_name="名称")
#     type = models.CharField(max_length=20, choices=permission_type_choices, default="menu", verbose_name="类型")
#     method = models.CharField(max_length=50, null=True, blank=True, verbose_name="方法")
#     pid = models.ForeignKey("Self", null=True, blank=True, on_delete=models.PROTECT, verbose_name='父级菜单')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = verbose_name = "权限"
#         ordering = ['id']


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField("Permission", blank=True, verbose_name="权限", related_name="role_permissions")
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单", related_name="role_menus")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")

    # content_type = models.ForeignKey(ContentType, '关联的表名称')
    #     # object_id = models.PositiveIntegerField()
    #     # content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "角色"


class Organization(models.Model):
    """
    组织架构
    """
    organization_type_choices = (
        ("company", "公司"),
        ("department", "部门")
    )
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=organization_type_choices, default="company", verbose_name="类型")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT,
                            verbose_name="父类组织", related_name="organization_pid")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = (
            ('add_organization', '添加部门'),
            ('change_organization', '修改部门'),
            ('delete_organization', '删除部门'),
            ('view_organization', '查看部门')
        )


class Position(models.Model):
    """
    岗位
    """
    name = models.CharField(max_length=20, default="", verbose_name="名称")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "岗位"


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    avatar = models.ImageField(upload_to="avatar/%Y%m%d/", default="avatar/default.jpg",
                               max_length=100, null=True, blank=True)
    department = models.ForeignKey("Organization", null=True, blank=True, on_delete=models.PROTECT, verbose_name="部门")
    position = models.ForeignKey("Position", null=True, blank=True,
                                 on_delete=models.PROTECT, verbose_name="职位", related_name="userProfile_position")
    superior = models.ForeignKey("self", null=True, blank=True,
                                 on_delete=models.PROTECT, verbose_name="上级主管", related_name="userProfile_superior")
    roles = models.ManyToManyField("Role", verbose_name="角色", blank=True, related_name="userProfile_roles")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = verbose_name = "用户信息"
        ordering = ['id', 'date_joined']

