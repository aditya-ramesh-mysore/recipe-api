from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email',)}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                    'is_staff'
                )
            }
        ),
        (
            'Important dates',
            {
                'fields' : (
                    'last_login',
                )
            }
        )
    )
    readonly_fields = ['last_login',]

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'name',
                    'password1',
                    'password2',
                    'is_active',
                    'is_superuser',
                    'is_staff',
                )
            }
        ),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)