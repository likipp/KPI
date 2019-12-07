from rest_framework import serializers

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

    def to_representation(self, instance):
        print(instance)
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
        return ret

    class Meta:
        model = GroupKPI
        fields = '__all__'


class KpiInputSerializers(serializers.ModelSerializer):
    """
        部门指标录入序列化
    """

    def to_representation(self, instance):
        user_name = instance.user.nickname
        group_kpi = instance.groupkpi
        ret = super(KpiInputSerializers, self).to_representation(instance)
        ret["status"] = group_kpi.get_status_display()
        ret["dep"] = group_kpi.dep.name
        ret["kpi"] = group_kpi.kpi.name
        ret["user"] = user_name
        ret['r_value'] = instance.r_value
        ret["t_value"] = group_kpi.t_value
        ret["l_limit"] = group_kpi.l_limit
        return ret

    class Meta:
        model = KpiInput
        fields = '__all__'
