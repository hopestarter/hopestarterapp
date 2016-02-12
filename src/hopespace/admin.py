from django.contrib.gis import admin
from hopespace.models import (
    LocationMark, Ethnicity, EthnicMember
)


class EthnicityAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )


class EthnicMemberAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'person')

admin.site.register(Ethnicity, EthnicityAdmin)
admin.site.register(EthnicMember, EthnicMemberAdmin)
admin.site.register(LocationMark, admin.OSMGeoAdmin)
