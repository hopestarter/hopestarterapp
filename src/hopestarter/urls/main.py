from django.conf.urls import include, url
from django.views.generic import TemplateView

from hopestarter.urls.admin import admin_patterns


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="index.html"), name="home"),
    url(r'^accounts/', include('allauth.urls')),
] + admin_patterns
