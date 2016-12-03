"""
Built-in, globally-available admin actions.
"""

from django.contrib.admin import helpers
from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.forms.widgets import Textarea
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

from hopespace.models import (
    LocationMark, Ethnicity, EthnicMember
)
from hopebase.util import (
    increment_user_post_count, decrement_user_post_count
)


class EthnicityAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', )


class EthnicMemberAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'person')


def censor_location_mark(modeladmin, request, queryset):
    if request.POST.get('post'):
        # user confirmed
        modeladmin.message_user(request, "Post censored")
        queryset.update(hidden=request.user)
        users = {m.user.id: m.user for m in queryset}
        for uid in users:
            decrement_user_post_count(users[uid])
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
    modeladmin.message_user(request, "Post uncensored")
    queryset.update(hidden=None)
    users = {m.user.id: m.user for m in queryset}
    for uid in users:
        increment_user_post_count(users[uid])
uncensor_location_mark.short_description = "Uncensor"


class LocationMarkAdmin(admin.GeoModelAdmin):
    readonly_fields = ('created', 'user', 'modified', 'hidden')
    list_display = ('__unicode__', 'user', 'large_picture', 'city', 'country',
                    'hidden')
    formfield_overrides = {
        models.PointField: {'widget': Textarea}
    }
    actions = [censor_location_mark, uncensor_location_mark]
    search_fields = ['^user__username', '^user__email', '=id']

    def get_urls(self):
        from django.conf.urls import url, patterns
        urls = super(LocationMarkAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(
                r'censor/(?P<mark_id>\d+)/',
                self.admin_site.admin_view(censor_location_mark_view),
                name='hopespace_locationmark_censor_location_mark',
            ),
        )
        return my_urls + urls


def censor_location_mark_view(request, mark_id):
    queryset = LocationMark.objects.filter(id=mark_id)
    modeladmin = admin.site._registry[LocationMark]
    response = censor_location_mark(modeladmin, request, queryset)
    if response is None:
        url = reverse('admin:hopespace_locationmark_changelist')
        return redirect('{}?q={}'.format(url, mark_id))
    return response


admin.site.register(Ethnicity, EthnicityAdmin)
admin.site.register(EthnicMember, EthnicMemberAdmin)
admin.site.register(LocationMark, LocationMarkAdmin)
