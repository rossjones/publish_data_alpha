
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, Http404


import drafts.forms as f
from userauth.logic import get_orgs_for_user
from drafts.models import Dataset, Datafile
from ckan_proxy.convert import draft_to_ckan, ckan_to_draft
from ckan_proxy.logic import (organization_show,
                              dataset_show,
                              dataset_create,
                              dataset_update)


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

    return render(request, "drafts/edit_title.html", {
        "form": form,
        "dataset": {},
    })


def edit_dataset_details(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    form = f.EditDatasetForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_organisation', [obj.name])

    return render(request, "drafts/edit_title.html", {
        "form": form,
        "dataset": dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def edit_organisation(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.OrganisationForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_licence',[obj.name])

    return render(request, "drafts/edit_organisation.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'organisations': get_orgs_for_user(request),
        'editing': request.GET.get('change', '') == '1',
    })


def edit_licence(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.LicenceForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_country', [obj.name])

    return render(request, "drafts/edit_licence.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def edit_country(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.CountryForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_frequency', [obj.name])

    return render(request, "drafts/edit_country.html", {
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

            # Determine where to route next based on the frequency value
            if obj.frequency in ['never', 'daily']:
                url = 'edit_dataset_addfile'
            elif obj.frequency in ['weekly']:
                url = 'edit_dataset_addfile_weekly'
            elif obj.frequency in ['quarterly']:
                url = 'edit_dataset_addfile_quarterly'
            elif obj.frequency in ['monthly']:
                url = 'edit_dataset_addfile_monthly'
            elif obj.frequency in ['annually']:
                url = 'edit_dataset_addfile_annually'

            return _redirect_to(request, url, [obj.name])


    return render(request, "drafts/edit_frequency.html", {
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

    return render(request, "drafts/edit_addfile.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_weekly(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.WeeklyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pass

    return render(request, "drafts/edit_addfile_week.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_monthly(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.MonthlyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pass

    return render(request, "drafts/edit_addfile_month.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_quarterly(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.QuarterlyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pass

    return render(request, "drafts/edit_addfile_quarter.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_addfile_annually(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.AnnuallyFileForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            pass

    return render(request, "drafts/edit_addfile_year.html", {
        'form': form,
        'dataset': dataset.as_dict(),
    })


def edit_files(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    viewname = 'edit_dataset_addfile'

    return render(request, "drafts/show_files.html", {
        'addfile_viewname': viewname,
        'dataset': dataset,
        'editing': request.GET.get('change', '') == '1',
    })


def edit_notifications(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.NotificationsForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_check_dataset',[obj.name])

    return render(request, "drafts/edit_notifications.html", {
        'form': form,
        'dataset': dataset.as_dict(),
        'editing': request.GET.get('change', '') == '1',
    })


def check_dataset(request, dataset_name):
    try:
        dataset = Dataset.objects.get(name=dataset_name)
    except Dataset.DoesNotExist:
        # Try and load the dataset from the live CKAN
        dataset = ckan_to_draft(dataset_name)

    organisation = organization_show(dataset.organisation)

    if request.method == 'POST':
        f = dataset_update \
            if dataset_show(dataset.name, request.user) \
            else dataset_create

        try:
            f(draft_to_ckan(dataset), request.user)
        except Exception as e:
            # TODO: Handle the error correctly
            print(e)
        else:
            # Success! We can safely delete the draft now
            dataset.delete()

        return HttpResponseRedirect('/manage?newset=1')


    return render(request, "drafts/check_dataset.html", {
        'dataset': dataset,
        'organisation': organisation
    })


def _redirect_to(request, url_name, args):
    if request.POST.get('editing') == "True":
        return HttpResponseRedirect(
            reverse('edit_dataset_check_dataset', args=args)
        )

    return HttpResponseRedirect(
        reverse(url_name, args=args)
    )
