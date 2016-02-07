from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from allauth.account.views import signup as allauth_signup

from hopestarter.urls.admin import admin_patterns


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="home"),
    url(r'^accounts/demo_signup/', csrf_exempt(allauth_signup), name="demo_signup"),
    url(r'^accounts/', include('allauth.urls')),
] + admin_patterns
