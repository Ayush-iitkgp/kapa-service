from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework_api_key.admin import APIKeyModelAdmin
from rest_framework_api_key.models import APIKey

from .models import Project, ProjectAPIKey, Team, User, UserEmailSettings

User = get_user_model()


class UserEmailSettingsInline(admin.StackedInline):
    model = UserEmailSettings
    can_delete = False
    verbose_name_plural = "email settings"


class UserAdminChangeForm(forms.ModelForm):
    """
    Form for editing the user in the admin panel. We are excluding the 'password' here because
    it can not be nullable and this would prohibit us from editing users that we do not want to give a password to.
    We are also excluding many fields that do not need to be changed. We are also do not allow editing the super user status
    because creation of super users should be forced from the command line because we can not edit passwords here.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_active",
            "team",
        )

    def __init__(self, *args, **kwargs):
        super(UserAdminChangeForm, self).__init__(*args, **kwargs)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm

    list_display = ("team", "email", "created_at")

    readonly_fields = (
        "is_superuser",
        "is_staff",
    )

    search_fields = ("email",)

    inlines = (UserEmailSettingsInline,)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")

    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "team",
        "project_name",
        "created_at",
    )

    search_fields = ("team__name", "project_name")

    ordering = ("-created_at",)


@admin.register(ProjectAPIKey)
class ProjectAPIKeyModelAdmin(APIKeyModelAdmin):
    list_display = [*APIKeyModelAdmin.list_display]


admin.site.unregister(APIKey)
