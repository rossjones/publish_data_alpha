from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.contrib.messages import constants as messages
from django import forms

from datasets.models import Dataset, Datafile, Organisation, Location


class DatafileInline(admin.TabularInline):
    model = Datafile


class DatasetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'title',
        'short_summary',
        'organisation',
        'published')
    list_filter = ('published',)
    search_fields = ('title', 'summary', 'description')
    inlines = [DatafileInline]

    def short_summary(self, obj):
        return obj.summary[0:120]
    short_summary.short_description = 'Summary'


class MoveDatasetsForm(ActionForm):
    new_organisation = forms.CharField(max_length=200)


def move_datasets(modeladmin, request, queryset):
    from datasets.search import index_dataset

    org_name = request.POST['new_organisation']
    try:
        neworg = Organisation.objects.get(name=org_name)
    except Organisation.DoesNotExist:
        return

    oldorg = queryset.all()[0]

    count = oldorg.datasets.count()
    ids = [str(d.id) for d in oldorg.datasets.all()]
    oldorg.datasets.update(organisation=neworg)
    modeladmin.message_user(
        request, "Successfully moved {} datasets from {} to {}".format(
            count, oldorg.title, neworg.title))

    for did in ids:
        ds = Dataset.objects.get(pk=did)
        index_dataset(ds)


move_datasets.short_description = 'Move datasets to new organisation'


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'abbreviation']
    search_fields = ['title', 'abbreviation']
    action_form = MoveDatasetsForm
    actions = [move_datasets]


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type']
    list_filter = ('location_type',)
    search_fields = ('name',)


admin.site.register(Location, LocationAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Organisation, OrganisationAdmin)
