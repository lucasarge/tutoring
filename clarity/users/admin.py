"""This is an admin file that is used to register the database models on the admin dashboard."""

from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin



# Important to be able to browse users and distinguish easily between them. Fieldsets displayed and filtering options.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("last_name", "first_name", "user_type", "email", "phone", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "user_type")

    ordering = ("last_name",)

    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "user_type")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "user_type", "email", "phone", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "first_name", "last_name")

# Registering database models for Service to the admin dashboard.
admin.site.register(Profile)
admin.site.register(CustomUser, CustomUserAdmin)