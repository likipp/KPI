from datetime import datetime

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework_guardian import filters as g_filter

from .models import KPI, GroupKPI, KpiInput, UserProfile, Organization
from .serializers import KPISerializers, GroupKPISerializers, KpiInputSerializers
from rbac.serializers.organization_serializer import OrganizationSerializer
from .filters import KPIFilter, GroupKPIFilter, KpiInputFilter
from utils.permissions import IsOwnerOrSuperUser, IsSuperUser, ReadOnly, CanPutAndUpdate
from utils.select import dash_list
from utils.pagination import BasePagination


class KPIViewSet(viewsets.ModelViewSet):
    """
        retrieve:
                返回指定KPI信息
        list:
                返回KPI列表
        update:
                更新KPI信息
        destroy:
                删除KPI记录
        create:
                创建KPI记录
        partial_update:
                更新记录部分字段
    """
    queryset = KPI.objects.all()
    pagination_class = BasePagination
    serializer_class = KPISerializers
    filterset_class = KPIFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name']

    @action(detail=True, methods=["get"], url_name="unused", url_path="unused")
    def get_unused(self, request, pk=None):
        ret = []
        kpiAll = []
        kpi = KPI.objects.exclude(status='disabled').all()
        for i in kpi:
            kpiAll.append(i)
        dep_queryset = Organization.objects.filter(name=request.query_params['dep']).all()
        # dep_queryset = Organization.objects.filter(name=request.data['dep']).all()
        for dep in dep_queryset:
            if dep.groupkpi_set.all():
                for groupkpi in dep.groupkpi_set.all():
                    if groupkpi.kpi in kpiAll:
                        kpiAll.remove(groupkpi.kpi)
            else:
                for kpi in kpiAll:
                    kpi_list = {"id": kpi.id, "name": kpi.name}
                    ret.append(kpi_list)
        for kpi in kpiAll:
            kpi_list = {"id": kpi.id, "name": kpi.name}
            ret.append(kpi_list)
        return Response(ret)


class GroupKPIEnabled(ListAPIView):
    queryset = KPI.objects.exclude(status='disabled').all()
    serializer_class = KPISerializers

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = KPISerializers(queryset, many=True)
        # serializer.is_valid()
        return Response(serializer.data)


class GroupKPIViewSet(viewsets.ModelViewSet):
    """
        retrieve:
                返回指定部门KPI信息
        list:
                返回部门KPI列表
        update:
                更新部门KPI信息
        destroy:
                删除部门KPI记录
        create:
                创建部门KPI记录
        partial_update:
                更新记录部分字段
    """
    pagination_class = BasePagination
    queryset = GroupKPI.objects.all()
    serializer_class = GroupKPISerializers
    permission_classes = [CanPutAndUpdate]
    filterset_class = GroupKPIFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, g_filter.ObjectPermissionsFilter)
    search_fields = ['dep__name', 'kpi__name']


class KpiInputViewSet(viewsets.ModelViewSet):
    """
            retrieve:
                    返回指定KPI录入信息
            list:
                    返回KPI录入信息列表
            update:
                    更新KPI录入信息
            destroy:
                    删除KPI录入记录
            create:
                    创建KPI录入记录
            partial_update:
                    更新记录部分字段
        """
    queryset = KpiInput.objects.all()
    serializer_class = KpiInputSerializers
    filterset_class = KpiInputFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['group_kpi__dep__name', 'group_kpi__kpi__name']
    # permission_classes = [CanPutAndUpdate | IsAuthenticated & ReadOnly | IsSuperUser]
    permission_classes = [CanPutAndUpdate]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return KpiInput.objects.all()
        else:
            return KpiInput.objects.filter(user=self.request.user)


class KpiDashViewSet(viewsets.ModelViewSet):
    queryset = KpiInput.objects.all()
    serializer_class = KpiInputSerializers
    serializer_dep = OrganizationSerializer
    serializer_groupkpi = GroupKPISerializers
    serializer_kpi = KPISerializers

    def get_queryset(self):
        if self.request.user.is_superuser:
            return KpiInput.objects.all()
        else:
            return KpiInput.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        ret = dict()
        dep_dict = dict()
        kpi = request.data.get('kpi') or None
        dep = request.data.get('dep')
        # dep = Organization.objects.filter(id=request.data.get('dep')).first().name
        if kpi:
            kpi_id = self.serializer_kpi.Meta.model.objects.filter(id=kpi).first()
            group_kpi = kpi_id.group_kpi.first()
            if request.user.is_superuser:
                input_list = group_kpi.input_group.all()
            else:
                input_list = group_kpi.input_group.filter(user=request.user)
            list_sort = dict()
            dash_list(input_list, list_sort, dep_dict, kpi_id)
            ret[dep] = dep_dict
            return Response(ret)
        else:
            groupkpi = GroupKPI.objects.filter(dep=dep)
            if groupkpi:
                for i in groupkpi:
                    if request.user.is_superuser:
                        input_list = i.input_group.all()
                    else:
                        input_list = i.input_group.filter(user=request.user)
                    list_sort = dict()
                    kpi = i.kpi
                    dash_list(input_list, list_sort, dep_dict, kpi)
                    ret[dep] = dep_dict
                return Response(ret)
            else:
                return Response('部门指标未创建', status=251)
