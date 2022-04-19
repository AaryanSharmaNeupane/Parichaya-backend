from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['mobile', 'name', 'email', ]
    fieldsets = (
        (None, {"fields": ('mobile', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'email',)}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2'),
        }),
    )


admin.site.register(models.User, UserAdmin)
