from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from hopebase.views import api
from hopecollector.views import UserLocationMarkView


urlpatterns = format_suffix_patterns([
    url(r'^profile/$',
        api.UserProfileView.as_view(),
        name='profile'),
    url(r'^mark/$',
        UserLocationMarkView.as_view(),
        name='user_marks'),
    url(r'^$',
        api.UserView.as_view(),
        name='account'),
]);
