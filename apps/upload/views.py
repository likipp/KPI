from django.shortcuts import render


from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UploadImage
from .serializers import UploadImageSerializer


class UploadImageViewSet(ModelViewSet):
    """
    上传图片列表
    """
    queryset = UploadImage.objects.all()
    serializer_class = UploadImageSerializer
    parser_classes = (MultiPartParser, FormParser,)

