from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from hopebase.views import api


urlpatterns = format_suffix_patterns([
    url(r'^profile/$',
        api.UserProfileView.as_view(),
        name='profile'),
]);
