from .web import *
from .space import *
from .log import *
from .aws import *
from .auth import *

INSTALLED_APPS += AUTH_INSTALLED_APPS

if 'django.contrib.sites' not in INSTALLED_APPS:
	INSTALLED_APPS += ('django.contrib.sites',)

if False:
	INSTALLED_APPS += ('debug_toolbar',
			   'django_extensions', )
	MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

SITE_ID = 1

GRAPPELLI_INDEX_DASHBOARD = 'hopestarter.dashboard.CustomIndexDashboard'

ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
