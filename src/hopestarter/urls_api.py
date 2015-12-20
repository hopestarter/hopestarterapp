from django.conf.urls import include, url

from hopestarter.api import api_root

import hopecollector.urls

urlpatterns = [
    url(r'^api/collector/', include(hopecollector.urls, namespace='collector', app_name='collector')),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', api_root, name="api_root"),
]
