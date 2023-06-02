from django.contrib import admin

from server.apps.groups import models


class GroupMemberInline(admin.TabularInline):
    """Group member tabular inline view for groups."""

    model = models.GroupMember
    extra = 0


class GroupAdmin(admin.ModelAdmin):
    """Group custom admin with tabular member inline."""
    inlines = [GroupMemberInline]
    list_display = ('name', 'created_at', 'id', 'get_members')

    def get_members(self, obj: models.Group):
        return list(obj.members.values_list('name', flat=True))

    get_members.short_description = 'Участники'


class GroupMemberAdmin(admin.ModelAdmin):
    """Group member custom admin."""

    list_display = ('name', 'role', 'group', 'user')


admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.GroupMember, GroupMemberAdmin)
