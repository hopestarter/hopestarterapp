"""
Built-in, globally-available admin actions.
"""

from django.contrib.admin import helpers
from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.forms.widgets import Textarea
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

from hopespace.models import (
    LocationMark, Ethnicity, EthnicMember
)


class EthnicityAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )


class EthnicMemberAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'person')


def censor_location_mark(modeladmin, request, queryset):
    if request.POST.get('post'):
        # user confirmed
        queryset.update(hidden=request.user)
        return None

    opts = modeladmin.model._meta
    if len(queryset) == 1:
        objects_name = force_text(opts.verbose_name)
    else:
        objects_name = force_text(opts.verbose_name_plural)

    context = dict(
        modeladmin.admin_site.each_context(request),
        title=_("Are you sure?"),
        objects_name=objects_name,
        action_name='censor_location_mark',
        queryset=queryset,
        opts=opts,
        action_checkbox_name=helpers.ACTION_CHECKBOX_NAME,
    )

    request.current_app = modeladmin.admin_site.name

    # Display the confirmation page
    return TemplateResponse(request, [
        "admin/censor_selected_confirmation.html"
    ], context)
censor_location_mark.short_description = "Censor"


def uncensor_location_mark(modeladmin, request, queryset):
    queryset.update(hidden=None)
uncensor_location_mark.short_description = "Uncensor"


class LocationMarkAdmin(admin.GeoModelAdmin):
    readonly_fields = ('created', 'user', 'modified', 'hidden')
    list_display = ('__unicode__', 'user', 'large_picture', 'city', 'country',
                    'hidden')
    formfield_overrides = {
        models.PointField: {'widget': Textarea}
    }
    actions = [censor_location_mark, uncensor_location_mark]


admin.site.register(Ethnicity, EthnicityAdmin)
admin.site.register(EthnicMember, EthnicMemberAdmin)
admin.site.register(LocationMark, LocationMarkAdmin)
