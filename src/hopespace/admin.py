from django.contrib.gis import admin
from hopespace.models import LocationMark


admin.site.register(LocationMark, admin.OSMGeoAdmin)
