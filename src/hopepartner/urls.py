from django.conf.urls import url

from hopepartner import views


urlpatterns = [
    url(r'^vetting/$',
        views.vetting,
        name='vetting'),
]
