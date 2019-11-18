from rest_framework.viewsets import ModelViewSet

from ..models import Position
from ..serializers.position_serializer import PositionSerializers
from utils.pagination import BasePagination


class PositionViewSet(ModelViewSet):
    pagination_class = BasePagination
    queryset = Position.objects.all()
    serializer_class = PositionSerializers
