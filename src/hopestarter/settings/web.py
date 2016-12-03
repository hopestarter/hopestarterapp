from .world import *

INSTALLED_APPS += (
    'django.contrib.humanize',
)

MAP_BOUNDARY_OFFSET = 0.1  # Boundary offset = 10%
MAP_MIN_ZOOM = 0.01        # Minimum degrees to show

from .secret import *
