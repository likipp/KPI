from rest_framework import routers

from django.urls import path, include

from .views import KPIViewSet, GroupKPIViewSet, KpiDashViewSet, GroupKPIEnabled

router = routers.SimpleRouter()
router.register('kpi', KPIViewSet, base_name='kpi')
router.register('group_kpi', GroupKPIViewSet, base_name='group_kpi')
router.register('dash', KpiDashViewSet, base_name='dash')
# router.register("kpiinput", KpiInputViewset, base_name="kpiinput")

urlpatterns = [
    path('', include(router.urls)),
    path('kpi_enabled/', GroupKPIEnabled.as_view(), name='kpi_enabled')
]
