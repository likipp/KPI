from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 1000
    page_size = 10


class TreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    # title = serializers.CharField(max_length=20, source='name')
    # organization_type_choices = (
    #     ("company", "公司"),
    #     ("department", "部门")
    # )
    # type = serializers.ChoiceField(choices=organization_type_choices, source="get_type_display")
    pid = serializers.PrimaryKeyRelatedField(read_only=True)


class TreeAPIView(ListAPIView):
    serializer_class = TreeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                    print(parent)
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)
