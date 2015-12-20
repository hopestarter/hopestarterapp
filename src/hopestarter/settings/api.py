from .base import *

try:
    from .drf import *
except ImportError:
    pass

ROOT_URLCONF = 'hopestarter.urls_api'

INSTALLED_APPS += (
    'rest_framework',
    'rest_framework_gis',
    'hopecollector',
)
