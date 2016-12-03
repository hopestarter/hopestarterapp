from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.conf import settings

from hopespace.models import LocationMark
from hopebase.models import UserProfile

BOUNDARY_OFFSET = 0.1  # Boundary offset = 10%


class LocationMarkListView(ListView):

    def get_queryset(self):
        qs = LocationMark.objects.exclude(user__profile=None)
        qs = qs.order_by('-created')
        qs = qs.select_related('user')
        qs = qs.prefetch_related('user__membership')
        return qs

    def get_context_data(self, **kwargs):
        context = super(LocationMarkListView, self).get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_MAPS_KEY

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

        min_lat = min([m.point.x for m in user_marks])
        max_lat = max([m.point.x for m in user_marks])
        min_lng = min([m.point.y for m in user_marks])
        max_lng = max([m.point.y for m in user_marks])

        context['view_boundary'] = {
            'north': min_lat - (max_lat - min_lat) * BOUNDARY_OFFSET,
            'east': max_lng + (max_lng - min_lng) * BOUNDARY_OFFSET,
            'south': max_lat + (max_lat - min_lat) * BOUNDARY_OFFSET,
            'west': min_lng - (max_lng - min_lng) * BOUNDARY_OFFSET
        }

        context['google_api_key'] = settings.GOOGLE_MAPS_KEY

        return context
