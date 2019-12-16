from django.db import models
from django.contrib.auth.models import Permission
from django.utils import timezone

from rbac.models import UserProfile, Organization


class KPI(models.Model):
    STATUS = {
        ('using', '使用中'),
        ('unused', '未使用'),
        ('disabled', '禁用')
    }
    name = models.CharField('名称', max_length=100)
    unit = models.CharField('单位', max_length=32)
    in_time = models.CharField('录入时间', max_length=32)
    mo_time = models.CharField('修改时间', max_length=32)
    status = models.CharField('状态', max_length=32, default='unused', choices=STATUS)

    class Meta:
        verbose_name_plural = verbose_name = "KPI"
        ordering = ["id", "name"]

    def __str__(self):
        return self.name


class GroupKPI(models.Model):
    STATUS = {
        ('using', '使用中'),
        ('unused', '未使用'),
        ('disabled', '禁用')
    }
    dep = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='所属部门', null=True, blank=True)
    kpi = models.ForeignKey(KPI, verbose_name='KPI',on_delete=models.CASCADE, related_name='group_kpi')
    u_limit = models.FloatField('上限值', max_length=10)
    l_limit = models.FloatField('下限值', max_length=10)
    t_value = models.FloatField('目标值', max_length=10)
    status = models.CharField('状态', default='unused', choices=STATUS, max_length=10)

    class Meta:
        verbose_name_plural = verbose_name = "部门KPI"
        ordering = ["id", "dep"]
        default_permissions = ()
        permissions = (
            ('add_groupkpi', '添加部门KPI'),
            ('change_groupkpi', '修改部门KPI'),
            ('delete_groupkpi', '删除部门KPI'),
            ('view_groupkpi', '查看部门KPI')
        )

    def __str__(self):
        return '{}_{}'.format(self.dep, self.kpi.name)

    @property
    def name(self):
        return '{}-{}'.format(self.dep, self.kpi.name)


class KpiInput(models.Model):
    r_value = models.FloatField('实际值', max_length=10)
    month = models.DateField('月份')
    add_time = models.DateTimeField('录入时间', auto_now_add=True)
    update_time = models.DateTimeField('最后修改时间', auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='录入人',
                             null=True, blank=True, related_name='input_user')
    group_kpi = models.ForeignKey(GroupKPI, on_delete=models.CASCADE, verbose_name='部门KPI',
                                  null=True, blank=True, related_name='input_group')

    class Meta:
        verbose_name_plural = verbose_name = "KPI数据输入"
        ordering = ["month"]
        default_permissions = ()
        permissions = (
            ('add_kpiinput', '添加数据'),
            ('change_kpiinput', '修改数据'),
            ('delete_kpiinput', '删除数据'),
            ('view_kpiinput', '查看数据')
        )

    def __str__(self):
        return '{}_{}'.format(self.user, self.group_kpi)


# class GuardianPermission(models.Model):
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限', null=True, blank=True)
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
