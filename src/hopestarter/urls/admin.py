from django.conf.urls import include, url
from django.contrib import admin


admin_patterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

