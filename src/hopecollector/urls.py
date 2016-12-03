from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from hopecollector import views


urlpatterns = format_suffix_patterns([
    url(r'^marks/$',
        views.LocationMarkView.as_view(),
        name='locationmark'),
    url(r'^mark/$',
        views.UserLocationMarkView.as_view(),
        name='user_marks'),
    url(r'^image/(?P<pk>\d+)/$',
        views.upload_image,
        name='mark_image'),
])
