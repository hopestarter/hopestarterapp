from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings

from hopespace.models import LocationMark
from hopebase.models import UserProfile


def get_common_map_context_data():
    return {
        'google_api_key': settings.GOOGLE_MAPS_KEY,
        'mark_opts': LocationMark._meta
    }


class LocationMarkListView(ListView):

    def get_queryset(self):
        qs = LocationMark.objects.snap_to_grid(0.005)
        qs = qs.exclude(user__profile=None)
        qs = qs.filter(Q(hidden=None) | Q(user_id=self.request.user.id))
        qs = qs.order_by('-created')
        qs = qs.select_related('user')
        qs = qs.select_related('user__profile')
        qs = qs.prefetch_related('user__membership')
        qs = qs.prefetch_related('user__vetting_set')
        return qs

    def get_context_data(self, **kwargs):
        context = super(LocationMarkListView, self).get_context_data(**kwargs)
        context.update(get_common_map_context_data())

        return context


class UserProfileView(DetailView):

    model = UserProfile

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username']).profile

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user_marks = context['user_marks'] = obj.user.marks.snap_to_grid(0.005)
        context['user'] = obj.user
        min_lng, min_lat, max_lng, max_lat = user_marks.extent()

        lat_span = max_lat - min_lat
        lng_span = max_lng - min_lng
        lat_offset = max(
            settings.MAP_MIN_ZOOM, lat_span * settings.MAP_BOUNDARY_OFFSET)
        lng_offset = max(
            settings.MAP_MIN_ZOOM, lng_span * settings.MAP_BOUNDARY_OFFSET)
        context['view_boundary'] = {
            'north': min_lat - lat_offset,
            'south': max_lat + lat_offset,
            'east': max_lng + lng_offset,
            'west': min_lng - lng_offset,
        }

        context.update(get_common_map_context_data())

        return context
