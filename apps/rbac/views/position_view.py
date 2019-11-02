from rest_framework.viewsets import ModelViewSet
from ..models import Position
from ..serializers.position_serializer import PositionSerializers


class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializers
