from django.contrib import admin

from datasets.models import Dataset, Datafile, Organisation, Location


class DatafileInline(admin.TabularInline):
    model = Datafile


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'short_summary', 'organisation', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'summary', 'description')
    inlines = [DatafileInline]

    def short_summary(self, obj):
        return obj.summary[0:120]
    short_summary.short_description = 'Summary'


admin.site.register(Dataset, DatasetAdmin)


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'abbreviation']
    search_fields = ['title', 'abbreviation']

admin.site.register(Organisation, OrganisationAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type']
    list_filter = ('location_type',)
    search_fields = ('name',)

admin.site.register(Location, LocationAdmin)
