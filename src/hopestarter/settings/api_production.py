import raven
from .api import *
from .utils import get_env_variable

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['api-test.hopestarter.org',]

INSTALLED_APPS += ("raven.contrib.django.raven_compat",)

MIDDLEWARE_CLASSES = (
  'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
  'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
) + MIDDLEWARE_CLASSES

RAVEN_CONFIG = {
    'dsn': RAVEN_DSN
}

SECRET_KEY = get_env_variable("SECRET_KEY")

# removing the browsable API - comment the following lines if you WANT the
# browsable API in production.
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ('rest_framework.renderers.JSONRenderer',)
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    'oauth2_provider.ext.rest_framework.OAuth2Authentication',
)
LOCATION_PERMS = ['IsAuthenticated', 'TokenHasScope']
PROFILE_PERMS = ['IsAuthenticated', 'TokenHasScope']
# end browsable API disabled settings

LOGGING['handlers']['file'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': '/var/log/nginx/api.log',
}
LOGGING['loggers']['django']['handlers'] = ['file']
