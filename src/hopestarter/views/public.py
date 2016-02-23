from django.views.generic import ListView
from hopespace.models import LocationMark


class LocationMarkListView(ListView):


    def get_queryset(self):
        qs = LocationMark.objects.exclude(user__profile=None)
        qs = qs.order_by('-created')
        qs = qs.select_related('user')
        qs = qs.prefetch_related('user__membership')
        return qs
