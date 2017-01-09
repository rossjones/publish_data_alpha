from django.contrib import admin

from .models import Organisation

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'abbreviation']
    search_fields = ['title', 'abbreviation']

admin.site.register(Organisation, OrganisationAdmin)
