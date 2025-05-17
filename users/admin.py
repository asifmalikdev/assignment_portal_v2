from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role','school', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'school')
    ordering = ('email','school')
    search_fields = ('email', 'full_name',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Roles & Permissions', {'fields': ('role', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2','school', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(User, UserAdmin)
