from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from server.apps.groups.admin import GroupMemberInline
from server.apps.users.models import User


class UserAdmin(admin.ModelAdmin):
    """Custom user admin."""

    form = ModelForm
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': (
            'username',
            'first_name',
            'last_name',
        )}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    inlines = [GroupMemberInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
