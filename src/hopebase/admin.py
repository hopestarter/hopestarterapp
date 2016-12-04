from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from hopebase.models import (
    UserProfile, Organization, OrganizationMembership, Vetting
)


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('name', 'surname', 'bitcoin', 'created', 'modified', 'user',
              'picture_tag', 'picture', 'signup')
    readonly_fields = ('created', 'modified', 'user', 'picture_tag')


class OrganizationMembershipInline(admin.TabularInline):
    model = OrganizationMembership
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    fields = ('name', 'owner', 'created', 'modified', 'id')
    readonly_fields = ('created', 'modified', 'id')
    inlines = (OrganizationMembershipInline,)


class OrganizationMembershipAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    search_fields = ('^person__username', '^organization__name')


class RevokedFilter(admin.SimpleListFilter):
    title = _('revoked')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'revoked'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('true', _('true')),
            ('false', _('false')),
            ('any', _('any')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'true':
            return queryset.exclude(revoked=None)
        if self.value() == 'false':
            return queryset.filter(revoked=None)
        return queryset


class VettingAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    ordering_fields = ('created', 'modified')
    list_filter = (RevokedFilter,)
    search_fields = ('^subject__username', '^organization__name',
                     '^reviewer__person__username')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMembership, OrganizationMembershipAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Vetting, VettingAdmin)
