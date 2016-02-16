from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from hopecollector import views


urlpatterns = format_suffix_patterns([
    url(r'^mark/$',
        views.LocationMarkSubmitView.as_view(),
        name='locationmark'),
    url(r'^uploadimage/$',
        views.upload_image,
        name='uploadimage'),
]);
