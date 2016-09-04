from django.contrib import admin
from hopebase.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('name', 'surname', 'bitcoin', 'created', 'modified', 'user', 'picture_tag')
    readonly_fields = ('created', 'modified', 'user', 'picture_tag')


admin.site.register(UserProfile, UserProfileAdmin)
