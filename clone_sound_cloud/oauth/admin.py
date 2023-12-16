from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, SocialLink, UserFollowing


class SocialLinkInLine(admin.TabularInline):
    model = SocialLink


class UserFollowingInLine(admin.TabularInline):
    model = UserFollowing
    fk_name = "user"


class UserProfileInLine(admin.TabularInline):
    model = UserProfile


@admin.register(User)
class UserAdmin(UserAdmin):
    """Define the admin pages for users."""
    model = User
    list_display = (
        "id", "email", "first_name", "last_name",
        "is_active", "is_staff", "is_spam_email")
    list_filter = ("email", "is_staff", "is_active", "is_spam_email")
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name",
                           "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_spam_email",
                                    "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2",
                "first_name", "last_name", "is_staff",
                "is_active", "is_spam_email", "groups", "user_permissions"
            )}
         ),
    )
    list_display_links = ('id', 'email',)
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'display_name', 'join_date',)
    list_display_links = ('id', 'user',)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'link',)


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'following_user', 'created_at',)
