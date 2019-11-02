from django_filters import rest_framework as filters

from .models import Organization, UserProfile
from utils.basefilter import ListFilter


class OrganizationFilter(filters.FilterSet):
    """
    Organization搜索类
    """
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Organization
        fields = ['name']


class UserFilter(filters.FilterSet):
    """
    用户搜索类
    """
    username = filters.CharFilter(lookup_expr="icontains", field_name="username")
    name = filters.CharFilter(lookup_expr="icontains", field_name="name")
    # dep = filters.ModelChoiceFilter(queryset=Organization.objects.all())
    department = ListFilter(field_name="department__name", lookup_expr="in")

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'department']
