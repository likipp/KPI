from datetime import datetime

from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import KPI, GroupKPI, KpiInput, UserProfile, Organization
from .serializers import KPISerializers, GroupKPISerializers, KpiInputSerializers
from rbac.serializers.organization_serializer import OrganizationSerializer
from .filters import KPIFilter, GroupKPIFilter, KpiInputFilter
from utils.permissions import IsOwner, IsSuperUser
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
                        for kpi in kpiAll:
                            kpi_list = {"id": kpi.id, "name": kpi.name}
                            ret.append(kpi_list)
            else:
                for kpi in kpiAll:
                    kpi_list = {"id": kpi.id, "name": kpi.name}
                    ret.append(kpi_list)
        print(ret)
        return Response(ret)

# class KPIUnUsed(ListAPIView):
#     queryset = KPI.objects.exclude(status='disabled').all()


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
    queryset = GroupKPI.objects.all()
    pagination_class = BasePagination
    serializer_class = GroupKPISerializers
    filterset_class = GroupKPIFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['dep__name', 'kpi__name']

    # def create(self, request, *args, **kwargs):
    #     dep = request.data['dep']
    #     has_kpi = GroupKPI.objects.filter(request.data['dep']).all()
    #     if has_kpi:
    #         kpi = GroupKPI.objects.exclude(request.data['dep'])
    #     print(request.data)
    #     pass


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
    search_fields = ['groupkpi__dep__name', 'groupkpi__kpi__name']
    permission_classes = (IsOwner,)

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
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return KpiInput.objects.all()
        else:
            return KpiInput.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        ret = dict()
        dep_dict = dict()
        kpi = request.data.get('kpi') or None
        kpi_id = self.serializer_kpi.Meta.model.objects.filter(name=kpi).first()
        dep = self.serializer_dep.Meta.model.objects.filter(name=request.data.get('name')).first().id
        if kpi:
            group_kpi = kpi_id.group_kpi.first()
            if request.user.is_superuser:
                input_list = group_kpi.input_group.all()
            else:
                input_list = group_kpi.input_group.filter(user=request.user)
            list_sort = dict()
            dash_list(input_list, list_sort, dep_dict, kpi)
            ret[dep] = dep_dict
        else:
            groupkpi = GroupKPI.objects.filter(dep=dep)
            for i in groupkpi:
                if request.user.is_superuser:
                    input_list = i.input_group.all()
                else:
                    input_list = i.input_group.filter(user=request.user)
                list_sort = dict()
                kpi = i.kpi.name
                dash_list(input_list, list_sort, dep_dict, kpi)
                ret[dep] = dep_dict
        return Response(ret)
