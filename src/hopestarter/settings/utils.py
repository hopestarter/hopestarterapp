import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name, default=None):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

def generate_celery_schedule(apps):
    """Gera um schedule dinamico para todas as apps"""
    schedule = {}

    for app in apps:

        schedule_module = "{0}.schedule".format(app)
        
        try:
            module = import_module(schedule_module)
        except ImportError:
            continue

        tempSchedule = getattr(module, "CELERYBEAT_SCHEDULE", None)
        if tempSchedule:
            schedule.update(tempSchedule)

    return schedule
