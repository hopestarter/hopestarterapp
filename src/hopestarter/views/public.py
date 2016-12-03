from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings

from hopespace.models import LocationMark
from hopebase.models import UserProfile

BOUNDARY_OFFSET = 0.1  # Boundary offset = 10%


def get_common_map_context_data():
    return {
        'google_api_key': settings.GOOGLE_MAPS_KEY,
        'mark_opts': LocationMark._meta
    }


class LocationMarkListView(ListView):

    def get_queryset(self):
        qs = LocationMark.objects.exclude(user__profile=None)
        qs = qs.filter(Q(hidden=None) | Q(user_id=self.request.user.id))
        qs = qs.order_by('-created')
        qs = qs.select_related('user')
        qs = qs.prefetch_related('user__membership')
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
        user_marks = context['user_marks'] = obj.user.marks.all()
        context['user'] = obj.user
        min_lng, min_lat, max_lng, max_lat = user_marks.extent()

        lat_offset = max(1, (max_lat - min_lat) * BOUNDARY_OFFSET)
        lng_offset = max(1, (max_lng - min_lng) * BOUNDARY_OFFSET)
        context['view_boundary'] = {
            'north': min_lat - lat_offset,
            'south': max_lat + lat_offset,
            'east': max_lng + lng_offset,
            'west': min_lng - lng_offset,
        }

        context.update(get_common_map_context_data())

        return context
