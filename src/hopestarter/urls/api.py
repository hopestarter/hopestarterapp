from django.conf.urls import (
    include, url, handler400, handler403, handler404, handler500)

from hopestarter.views.api import api_root
from hopestarter.urls.admin import admin_patterns

import hopecollector.urls

urlpatterns = [
	url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/collector/', include(hopecollector.urls, namespace='collector', app_name='collector')),
	url(r'^api/auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/user/', include('hopebase.urls', namespace="base")),
    url(r'^api/', api_root, name="api_root"),
] + admin_patterns

handler400 = 'hopecollector.views.bad_request'
handler403 = 'hopecollector.views.permission_denied'
handler404 = 'hopecollector.views.page_not_found'
handler500 = 'hopecollector.views.server_error'
