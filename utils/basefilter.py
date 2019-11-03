import django_filters


class ListFilter(django_filters.CharFilter):

    def filter(self, qs, value):
        value = list(filter(None, value.split(",")))
        return super(ListFilter, self).filter(qs=qs, value=value)
