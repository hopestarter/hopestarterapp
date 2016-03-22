import django_filters

from rest_framework.filters import FilterSet

from hopespace.models import LocationMark


class LocationMarkFilterSet(FilterSet):
    after = django_filters.IsoDateTimeFilter(name="created", lookup_type='gte')
    before = django_filters.IsoDateTimeFilter(name="created", lookup_type='lte')

    class Meta:
        model = LocationMark
        fields = ['created']
