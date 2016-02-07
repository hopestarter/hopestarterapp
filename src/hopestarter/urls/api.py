from django.conf.urls import include, url
from django.contrib import admin

from hopestarter.api import api_root

import hopecollector.urls

urlpatterns = [
	url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/collector/', include(hopecollector.urls, namespace='collector', app_name='collector')),
	url(r'^api/auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', api_root, name="api_root"),
    url(r'^admin/', include(admin.site.urls)),
]
