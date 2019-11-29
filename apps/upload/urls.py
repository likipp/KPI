from rest_framework import routers

from django.urls import path, include

from .views import UploadImageViewSet

router = routers.SimpleRouter()
router.register('upload', viewset=UploadImageViewSet, base_name='upload')

urlpatterns = [
    path('', include(router.urls))
]
