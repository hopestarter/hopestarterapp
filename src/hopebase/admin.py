from django.contrib import admin
from hopebase.models import (
    UserProfile, Organization, OrganizationMembership
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


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMembership, OrganizationMembershipAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
