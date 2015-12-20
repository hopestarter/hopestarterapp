from django.apps import AppConfig


class HopeSpaceConfig(AppConfig):

    name = 'hopespace'
    verbose_name = 'Hopestarter Spatial Data'

    def ready(self):
        import hopespace.signals
