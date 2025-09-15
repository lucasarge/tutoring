from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("last_name", "first_name", "email", "phone", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")

    ordering = ("last_name",)

    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "first_name", "last_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "first_name", "last_name")
    
admin.site.register(CustomUser, CustomUserAdmin)