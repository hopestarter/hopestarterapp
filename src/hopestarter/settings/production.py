import raven
from .world import *
from .utils import get_env_variable
from .api_secret import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = []

INSTALLED_APPS += ("raven.contrib.django.raven_compat",)

MIDDLEWARE_CLASSES = (
  'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
  'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
) + MIDDLEWARE_CLASSES

RAVEN_CONFIG = {
    'dsn': RAVEN_DSN,
    'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}

SECRET_KEY = get_env_variable("SECRET_KEY")

SITE_ID = 1

GRAPPELLI_INDEX_DASHBOARD = 'hopestarter.dashboard.CustomIndexDashboard'
