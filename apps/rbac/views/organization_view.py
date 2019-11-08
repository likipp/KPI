from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Organization
from ..serializers.organization_serializer import OrganizationSerializer,\
    OrganizationUserTreeSerializer, OrganizationTreeSerializer
from utils.baseviews import BasePagination
from utils.baseviews import TreeAPIView


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = BasePagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)


class OrganizationTreeView(TreeAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationTreeSerializer


class OrganizationUserTreeView(APIView):

    def get(self, request, format=None):
        organizations = Organization.objects.all()
        serializer = OrganizationUserTreeSerializer(organizations, many=True)
        tree_dict = {}
        tree_data = []
        for item in serializer.data:
            new_item = {
                'id': 'o' + str(item['id']),
                'title': item['label'],
                'label': item['label'],
                'pid': item['pid'],
                'children': item['children']
            }
            tree_dict[item['id']] = new_item
        for i in tree_dict:
            if tree_dict[i]['pid']:
                pid = tree_dict[i]['pid']
                parent = tree_dict[pid]
                parent['children'].append(tree_dict[i])
            else:
                tree_data.append(tree_dict[i])
        return Response(tree_data)
