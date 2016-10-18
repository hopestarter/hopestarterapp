from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.forms.widgets import Textarea

from hopespace.models import (
    LocationMark, Ethnicity, EthnicMember
)


class EthnicityAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )


class EthnicMemberAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'person')

class LocationMarkAdmin(admin.GeoModelAdmin):
    readonly_fields = ('created', 'user')
    list_display = ('__unicode__', 'user', 'large_picture',)
    formfield_overrides = {
        models.PointField: {'widget': Textarea }
    }


admin.site.register(Ethnicity, EthnicityAdmin)
admin.site.register(EthnicMember, EthnicMemberAdmin)
admin.site.register(LocationMark, LocationMarkAdmin)
