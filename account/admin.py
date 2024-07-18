from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_groups', 'is_active')
    list_filter = ('is_active', 'groups')

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
