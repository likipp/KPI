from rest_framework import serializers
from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin

from .models import KPI, GroupKPI, KpiInput


class KPISerializers(serializers.ModelSerializer):
    """
        KPI序列化
    """
    def to_representation(self, instance):
        ret = super(KPISerializers, self).to_representation(instance)
        status = instance.status
        status_name = instance.get_status_display()
        ret['status'] = {
            'id': status,
            'name': status_name
        }
        return ret

    class Meta:
        model = KPI
        fields = '__all__'


class GroupKPISerializers(serializers.ModelSerializer):
    """
        部门KPI序列化
    """
    # name = serializers.HiddenField(default='', read_only=True)

    def to_representation(self, instance):
        status = instance.status
        status_name = instance.get_status_display()
        dep_instance = instance.dep
        kpi_instance = instance.kpi
        ret = super(GroupKPISerializers, self).to_representation(instance)
        ret["in_time"] = kpi_instance.in_time
        ret["mo_time"] = kpi_instance.mo_time
        ret["status"] = {
            "id": status,
            "name": status_name
        }
        ret["dep"] = {
            "id": dep_instance.id,
            "name": dep_instance.name
        }
        ret["kpi"] = {
            "id": kpi_instance.id,
            "name": kpi_instance.name
        }
        # ret["name"] = instance.name
        return ret

    # def validate_name(self, pk, name):
    #     print(self, pk, name, 65322)
    #     if GroupKPI.objects.filter(id=pk).name == name:
    #         raise serializers.ValidationError(name + ' 部门KPI已存在')
    #     return name

    class Meta:
        model = GroupKPI
        fields = '__all__'

    # def get_permissions_map(self, created):
    #     current_user = self.content['request'].user
    #
    #     return {
    #         'view_groupkpi': [current_user]
    #     }
    #
    # def assign_permissions(self, permission_map):
    #     pass


class KpiInputSerializers(serializers.ModelSerializer):
    """
        部门指标录入序列化
    """

    def to_representation(self, instance):
        if instance.group_kpi is not None:
            user_name = instance.user.name
            group_kpi = instance.group_kpi
            ret = super(KpiInputSerializers, self).to_representation(instance)
            ret["status"] = group_kpi.get_status_display()
            ret["dep"] = group_kpi.dep.name
            ret["kpi"] = group_kpi.kpi.name
            ret["user"] = user_name
            ret['r_value'] = instance.r_value
            ret["t_value"] = group_kpi.t_value
            ret["l_limit"] = group_kpi.l_limit
            return ret
        else:
            return []

    class Meta:
        model = KpiInput
        fields = '__all__'
