import os

if os.environ.get('LOGNAME')=='mpetyx':
    from .mpetyx_base import *
else:
    from .base import *
from .space import *
from .log import *
from .aws import *

try:
    from .drf import *
except ImportError:
    pass

ROOT_URLCONF = 'hopestarter.urls.api'

INSTALLED_APPS += (
    'storages',
    'oauth2_provider',
    'rest_framework',
    'rest_framework_gis',
    'social.apps.django_app.default',
    'rest_framework_social_oauth2',
    'django_filters',
    'hopecollector',
)

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'set-location': 'Set location',
        'update-profile': 'Update Profile'
    }
}

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SITE_ID = 2

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = True # use https
AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3-eu-west-1.amazonaws.com'
# see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

GRAPPELLI_INDEX_DASHBOARD = 'hopecollector.dashboard.CustomIndexDashboard'

LOCATION_PERMS = ['IsAuthenticated', 'WeakTokenHasScope']
PROFILE_PERMS = ['IsAuthenticated', 'WeakTokenHasScope']
ETHNICITY_PERMS = ['IsAuthenticated', 'WeakTokenHasScope']

if os.environ.get('LOGNAME')!='mpetyx':
    from .api_secret import *
