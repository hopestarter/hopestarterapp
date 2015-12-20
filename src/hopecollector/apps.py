from django.apps import AppConfig


class HopeCollectorConfig(AppConfig):

    name = 'hopecollector'
    verbose_name = 'Hopestarter Location Collector'

    def ready(self):
        import hopecollector.signals
