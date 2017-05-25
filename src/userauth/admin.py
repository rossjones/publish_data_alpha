from django.utils.translation import ugettext as _

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from userauth.models import PublishingUser


class OrganisationsInline(admin.TabularInline):
    model = PublishingUser.organisations.through
    extra = 1


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"), help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = PublishingUser
        exclude = ()

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    model = PublishingUser
    inlines = [OrganisationsInline]
    fieldsets = (
        (None, {'fields': ('email', 'apikey', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1',
                       'password2')}
         ),
    )


admin.site.register(PublishingUser, UserAdmin)
