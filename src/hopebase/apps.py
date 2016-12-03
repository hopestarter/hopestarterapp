from django.apps import AppConfig


class HopeBaseConfig(AppConfig):

    name = 'hopebase'
    verbose_name = 'Hopestarter Base Data'

    def ready(self):
        import hopebase.signals   # noqa
