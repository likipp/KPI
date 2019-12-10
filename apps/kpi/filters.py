from django_filters import rest_framework as filters

from rbac.models import Organization
from .models import KPI, GroupKPI, KpiInput


class GroupKPIFilter(filters.FilterSet):
    dep = filters.ModelChoiceFilter(queryset=Organization.objects.all())
    kpi = filters.ModelChoiceFilter(queryset=KPI.objects.all())

    class Meta:
        model = GroupKPI
        fields = ["dep", "kpi"]


class KPIFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    status = filters.CharFilter(lookup_expr="icontains", field_name="name")

    class Meta:
        model = KPI
        fields = ["name", "status"]


class KpiInputFilter(filters.FilterSet):
    group_kpi = filters.ModelChoiceFilter(queryset=GroupKPI.objects.all())
    kpi = filters.ModelChoiceFilter(queryset=KPI.objects.all())

    class Meta:
        model = KpiInput
        fields = ["group_kpi", "kpi"]