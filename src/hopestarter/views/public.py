from django.views.generic import ListView, DetailView
from hopespace.models import LocationMark
from hopebase.models import UserProfile


class LocationMarkListView(ListView):


    def get_queryset(self):
        qs = LocationMark.objects.exclude(user__profile=None)
        qs = qs.order_by('-created')
        qs = qs.select_related('user')
        qs = qs.prefetch_related('user__membership')
        return qs


class UserProfileView(DetailView):

    model = UserProfile

    def get_context_data(self, **kwargs):
        obj = super(UserProfileView, self).get_object()
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['user_marks'] = obj.user.marks.all()
        return context
