from django.contrib import admin

from rbac.models import UserProfile, Organization


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name')
    search_fields = ('username', 'name')
    filter_horizontal = ('roles',)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
