import django_filters

from rest_framework.filters import FilterSet

from hopespace.models import LocationMark


class LocationMarkFilterSet(FilterSet):
    after = django_filters.IsoDateTimeFilter(name="created", lookup_expr='gte')
    before = django_filters.IsoDateTimeFilter(name="created", lookup_expr='lte')

    class Meta(object):
        model = LocationMark
        fields = ['created', 'user']


class UserLocationMarkFilterSet(LocationMarkFilterSet):

    class Meta(LocationMarkFilterSet.Meta):
        fields = ['created']
