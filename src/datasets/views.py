from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, Http404


import datasets.forms as f
from datasets.logic import organisations_for_user
from datasets.models import Dataset, Datafile


def new_dataset(request):
    form = f.DatasetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = Dataset.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                summary=form.cleaned_data['summary'],
                creator=request.user,
                name=form.cleaned_data['name']
            )

            return HttpResponseRedirect(
                reverse('edit_dataset_organisation', args=[obj.name])
            )


    return render(request, "datasets/edit_title.html", {
        "form": form,
        "dataset": {},
    })


def edit_full_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.FullDatasetForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(
                reverse('manage_data') + "?edited=1"
            )

    return render(request, "datasets/edit_dataset.html", {
        "form": form,
        "dataset": dataset,
    })


def delete_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    dataset.delete()
    return HttpResponseRedirect(
        reverse('manage_data') + "?deleted=1"
    )


def edit_dataset_details(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    form = f.EditDatasetForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_organisation', [obj.name])

    return render(request, "datasets/edit_title.html", {
        "form": form,
        "dataset": dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def edit_organisation(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    organisations = organisations_for_user(request.user)
    if len(organisations) == 1:
        dataset.organisation = organisations[0]
        dataset.save()
        return _redirect_to(request, 'edit_dataset_licence',[dataset.name])

    form = f.OrganisationForm(request.POST or None, instance=dataset)
    form.fields["organisation"].queryset = request.user.organisation_set.all()

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_licence',[obj.name])

    return render(request, "datasets/edit_organisation.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'organisations': organisations,
        'editing': request.GET.get('change', '') == '1',
    })


def edit_licence(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.LicenceForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_location', [obj.name])

    return render(request, "datasets/edit_licence.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def edit_location(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.LocationForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_frequency', [obj.name])

    return render(request, "datasets/edit_location.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def edit_frequency(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.FrequencyForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            url = _frequency_redirect_to(obj)

            return _redirect_to(request, url, [obj.name])


    return render(request, "datasets/edit_frequency.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def edit_addfile(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.FileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            data['dataset'] = dataset
            obj = Datafile.objects.create(**data)
            obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_files', args=[dataset_name])
            )

    return render(request, "datasets/edit_addfile.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_weekly(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.WeeklyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            data['dataset'] = dataset
            obj = Datafile.objects.create(**data)
            obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_files', args=[dataset_name])
            )

    return render(request, "datasets/edit_addfile_week.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_monthly(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.MonthlyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            data['dataset'] = dataset
            obj = Datafile.objects.create(**data)
            obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_files', args=[dataset_name])
            )

    return render(request, "datasets/edit_addfile_month.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_quarterly(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.QuarterlyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            data['dataset'] = dataset
            obj = Datafile.objects.create(**data)
            obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_files', args=[dataset_name])
            )

    return render(request, "datasets/edit_addfile_quarter.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_annually(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.AnnuallyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            data['dataset'] = dataset
            obj = Datafile.objects.create(**data)
            obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_files', args=[dataset_name])
            )

    return render(request, "datasets/edit_addfile_year.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_files(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    url = _frequency_redirect_to(dataset)

    return render(request, "datasets/show_files.html", {
        'addfile_viewname': url,
        'dataset': dataset,
        'editing': request.GET.get('change', '') == '1',
    })


def edit_notifications(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if dataset.frequency in ['daily', 'never']:
        dataset.noficiations = 'no'
        dataset.save()

        return _redirect_to(request, 'edit_dataset_check_dataset',[dataset.name])

    form = f.NotificationsForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_check_dataset',[obj.name])

    return render(request, "datasets/edit_notifications.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def check_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    organisation = dataset.organisation
    organisations = organisations_for_user(request.user)
    single_organisation = len(organisations) == 1


    if request.method == 'POST':
        dataset.published = True
        dataset.published_date = datetime.now()
        dataset.save()

        return HttpResponseRedirect('/manage?newset=1')


    return render(request, "datasets/check_dataset.html", {
        'dataset': dataset,
        'licence': dataset.licence if dataset.licence != 'other' else dataset.licence_other,
        'organisation': organisation,
        'single_organisation': single_organisation
    })


def _frequency_redirect_to(dataset):
    frequency = dataset.frequency

    # Default to standard add file.
    url = 'edit_dataset_addfile'

    if frequency in ['never', 'daily']:
        url = 'edit_dataset_addfile'
    elif frequency in ['weekly']:
        url = 'edit_dataset_addfile_weekly'
    elif frequency in ['quarterly']:
        url = 'edit_dataset_addfile_quarterly'
    elif frequency in ['monthly']:
        url = 'edit_dataset_addfile_monthly'
    elif frequency in ['annually']:
        url = 'edit_dataset_addfile_annually'

    return url


def _redirect_to(request, url_name, args):
    if request.POST.get('editing') == "True":
        return HttpResponseRedirect(
            reverse('edit_dataset_check_dataset', args=args)
        )

    return HttpResponseRedirect(
        reverse(url_name, args=args)
    )
