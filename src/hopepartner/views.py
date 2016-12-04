from django.shortcuts import render

from hopebase.models import UserProfile


def vetting(request):
    return render(request, "vetting.html", context={
        'object_list': UserProfile.objects.filter(signup='app')
    })
