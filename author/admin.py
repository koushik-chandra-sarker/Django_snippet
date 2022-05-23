from django.contrib import admin

# Register your models here.
from author.form import UserCreationForm, UserChangeForm
from author.models.role_model import Role
from author.models.user_model import Profile, User, EmailConfirmed
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_superuser']
    fieldsets = (
        (
            None, {
                'fields': ('email', 'username', 'first_name', 'last_name', 'password')
            }
        ),
        (
            "Permission", {
                'fields': ('is_active', 'is_superuser', 'is_staff')
            }
        ), (
            "Role", {
                'fields': ('roles',)
            }
        ),
        (_('Group Permissions'), {
            'fields': ('groups', 'user_permissions',)
        }),
        (_('Important dates'), {'fields': ('last_login',)}),

    )
    add_fieldsets = (
        (
            None, {
                'fields': ('email', 'username', 'first_name', 'last_name', 'is_active', 'password1', 'password2')
            }
        ),
        (
            "Permission", {
                'fields': ('is_superuser', 'is_staff')
            }
        ),
    )
    ordering = ['email']
    search_fields = ['email']
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(EmailConfirmed)
class EmailConfirmedAdmin(BaseUserAdmin):
    list_display = ['user', 'first_name', 'last_name', 'activation_key', 'email_confirm', 'created_at']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    filter_horizontal = ()
    list_filter = []
    ordering = []
    search_fields = []


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

