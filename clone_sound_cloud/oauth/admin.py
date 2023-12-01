from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, Follower, SocialLink


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    """Define the admin pages for users."""
    model = User
    list_display = (
        "email", "first_name", "last_name",
        "is_active", "is_staff",)
    list_filter = ("email", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name",
                           "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active",
                                    "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2",
                "first_name", "last_name", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'join_date',)
    list_display_links = ('id',)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'link',)

