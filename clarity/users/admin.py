from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Profile)

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
    
admin.site.register(CustomUser, CustomUserAdmin)