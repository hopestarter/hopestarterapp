from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from django.core.urlresolvers import reverse

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from hopebase.models import (
    UserProfile, Organization, OrganizationMembership, Vetting
)


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


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False


class OrganizationMembershipInline(admin.StackedInline):
    model = OrganizationMembership
    extra = 0
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline, OrganizationMembershipInline]
    list_display = ('username', 'email', 'date_joined', 'last_login', 'profile_link')

    def profile_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:hopebase_userprofile_change", args=(obj.profile.pk,)), obj.profile))
    profile_link.short_description = 'profile'

    def get_queryset(self, request):
        return super(UserAdmin,self).get_queryset(request).prefetch_related('profile')


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('name', 'surname', 'bitcoin', 'created', 'modified',
              'picture_tag', 'picture', 'signup', 'user_link')
    readonly_fields = ('created', 'modified', 'picture_tag', 'user_link')
    list_display = ('name', 'surname', 'bitcoin', 'created', 'modified', 'user_link')

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.user.pk,)), obj.user))
    user_link.short_description = 'user'


class OrganizationMembershipInline(admin.TabularInline):
    model = OrganizationMembership
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    fields = ('name', 'owner', 'created', 'modified', 'id')
    readonly_fields = ('created', 'modified', 'id')
    inlines = (OrganizationMembershipInline,)


class OrganizationMembershipAdmin(admin.ModelAdmin):
    fields = ('organization', 'created', 'modified', 'revoked')
    readonly_fields = ('user_link', 'created', 'modified', 'organization')
    search_fields = ('^person__username', '^organization__name')
    list_display = ('user_link', 'organization', 'created', 'modified', 'revoked')
    list_filter = (RevokedFilter,)

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.person.pk,)), obj.person))
    user_link.short_description = 'user'


class VettingAdmin(admin.ModelAdmin):
    readonly_fields = ('subject_link', 'reviewer_link', 'created', 'reviewer', 'modified', 'organization')
    ordering_fields = ('created', 'modified')
    list_filter = (RevokedFilter,)
    search_fields = ('^subject__username', '^organization__name',
                     '^reviewer__person__username')
    list_display = ('subject_link', 'reviewer_link', 'organization', 'created', 'modified', 'revoked')

    def get_queryset(self, request):
        return super(VettingAdmin,self).get_queryset(request).select_related('subject', 'reviewer__person', 'organization')

    def subject_link(self, obj):
        return self.user_link(obj.subject)
    subject_link.short_description = 'subject'

    def reviewer_link(self, obj):
        return self.user_link(obj.reviewer.person)
    reviewer_link.short_description = 'reviewer'

    def user_link(self, user):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(user.pk,)), user))


user_model = get_user_model()
admin.site.unregister(user_model)
admin.site.register(user_model, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMembership, OrganizationMembershipAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Vetting, VettingAdmin)
