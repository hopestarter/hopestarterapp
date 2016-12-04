import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'stderr': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['stderr'],
            'level': os.environ.get('LOGLEVEL', 'INFO'),
            'propagate': True,
        },
        'hopebase': {
            'handlers': ['stderr'],
            'level': os.environ.get('LOGLEVEL', 'INFO'),
            'propagate': True,
        },
        'hopepartner': {
            'handlers': ['stderr'],
            'level': os.environ.get('LOGLEVEL', 'INFO'),
            'propagate': True,
        },
        'hopecollector': {
            'handlers': ['stderr'],
            'level': os.environ.get('LOGLEVEL', 'INFO'),
            'propagate': True,
        },
    },
}
