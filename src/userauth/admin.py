from django.utils.translation import ugettext as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from userauth.models import PublishingUser


class OrganisationsInline(admin.TabularInline):
    model = PublishingUser.organisations.through
    extra = 1



class UserAdmin(BaseUserAdmin):
    model = PublishingUser
    inlines = [OrganisationsInline]
    fieldsets = (
        (None, {'fields': ('email', 'apikey')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1',
                       'password2')}
         ),
    )


admin.site.register(PublishingUser, UserAdmin)
