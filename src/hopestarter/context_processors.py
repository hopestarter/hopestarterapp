from django.conf import settings

def template_settings(request):
    return {'DEFAULT_PROFILE_IMAGE': settings.DEFAULT_PROFILE_IMAGE}
