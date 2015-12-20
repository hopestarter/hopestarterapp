from .base import *

try:
    from .drf import *
except ImportError:
    pass

ROOT_URLCONF = 'hopestarter.urls_api'

INSTALLED_APPS += (
    'oauth2_provider',
    'rest_framework',
    'rest_framework_gis',
    'hopecollector',
)

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'set-location': 'Set location'}
}
