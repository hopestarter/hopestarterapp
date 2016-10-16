from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
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

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username']).profile

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['user_marks'] = obj.user.marks.all()
        return context
