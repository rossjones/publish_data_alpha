from django.contrib import admin

from datasets.models import Dataset, Datafile, Organisation


class DatafileInline(admin.TabularInline):
    model = Datafile


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [DatafileInline]


admin.site.register(Dataset, DatasetAdmin)


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'abbreviation']
    search_fields = ['title', 'abbreviation']

admin.site.register(Organisation, OrganisationAdmin)
