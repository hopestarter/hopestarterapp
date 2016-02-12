from django.contrib import admin
from hopebase.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'user',)


admin.site.register(UserProfile, UserProfileAdmin)
