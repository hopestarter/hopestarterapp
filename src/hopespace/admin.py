from django.contrib.gis import admin
from hopespace.models import (
    LocationMark, Ethnicity, EthnicMember
)


class EthnicityAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )


class EthnicMemberAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'person')

class LocationMarkAdmin(admin.OSMGeoAdmin):
    readonly_fields = ('created', 'user')
    list_display = ('__unicode__', 'user', 'large_picture',)

admin.site.register(Ethnicity, EthnicityAdmin)
admin.site.register(EthnicMember, EthnicMemberAdmin)
admin.site.register(LocationMark, LocationMarkAdmin)
