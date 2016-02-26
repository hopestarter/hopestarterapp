import raven
from .web import *
from .space import *
from .log import *
from .utils import get_env_variable
from .auth import *

INSTALLED_APPS += AUTH_INSTALLED_APPS

if 'django.contrib.sites' not in INSTALLED_APPS:
	INSTALLED_APPS += ('django.contrib.sites',)

try:
    from .api_secret import *
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN
    }
    INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
except ImportError:
    pass

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['staging.hopestarter.org']

MIDDLEWARE_CLASSES = (
  'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
  'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
) + MIDDLEWARE_CLASSES


SECRET_KEY = get_env_variable("SECRET_KEY")

SITE_ID = 1

GRAPPELLI_INDEX_DASHBOARD = 'hopestarter.dashboard.CustomIndexDashboard'

LOGGING['handlers']['file'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': '/var/log/nginx/django.log',
}
LOGGING['loggers']['django']['handlers'] = ['file']
