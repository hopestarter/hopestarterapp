from django.shortcuts import render

from hopebase.models import UserProfile


def vetting(request):
    profiles = UserProfile.objects.filter(signup='app')
    profiles = profiles.prefetch_related('user__vetting_set')
    return render(request, "vetting.html", context={
        'object_list': profiles
    })
