from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from allauth.account.views import signup as allauth_signup

from hopestarter.urls.admin import admin_patterns
from hopestarter.views.public import LocationMarkListView, UserProfileView


urlpatterns = [
    url(r"^$", LocationMarkListView.as_view(), name="home"),
    url(r"^profile/(?P<username>[-\w]+)$", UserProfileView.as_view(), name="user-profile"),
    url(r"^index/$", TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^accounts/demo_signup/', csrf_exempt(allauth_signup), name="demo_signup"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^partners/', include('hopepartner.urls')),
] + admin_patterns
