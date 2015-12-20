from .base import *
from .world import *
from .auth import *

INSTALLED_APPS += ('debug_toolbar',
                   'django_extensions', )
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

SITE_ID = 1
