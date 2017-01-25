from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, Http404

import datasets.forms as f
from datasets.auth import user_can_edit_dataset, user_can_edit_datafile
from datasets.logic import organisations_for_user, publish_to_ckan
from datasets.models import Dataset, Datafile
from datasets.search import index_dataset
from datasets.search import delete_dataset as unindex_dataset

def new_dataset(request):
    form = f.DatasetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = Dataset.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                summary=form.cleaned_data['summary'],
                creator=request.user
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
    organisations = organisations_for_user(request.user)
    url = _frequency_redirect_to(dataset)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    form = f.FullDatasetForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()

            # Re-publish if we are editing a published dataset
            err = publish_to_ckan(obj)
            if dataset.published:
                index_dataset(obj)
            else:
                unindex_dataset(obj)

            return HttpResponseRedirect(
                reverse('manage_data') + "?result=edited"
            )

    return render(request, "datasets/edit_dataset.html", {
        "addfile_viewname": url,
        "form": form,
        "dataset": dataset,
        "organisations": organisations,
    })


def delete_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    unindex_dataset(dataset)
    dataset.delete()

    return HttpResponseRedirect(
        reverse('manage_data') + "?result=deleted"
    )


def edit_dataset_details(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    form = f.EditDatasetForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(
                request,
                'edit_dataset_organisation',
                [obj.name]
            )

    return render(request, 'datasets/edit_title.html', {
        'form': form,
        'dataset': dataset,
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_organisation(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    organisations = organisations_for_user(request.user)
    if len(organisations) == 1:
        dataset.organisation = organisations[0]
        dataset.save()
        return _redirect_to(request, 'edit_dataset_licence',[dataset.name])

    form = f.OrganisationForm(request.POST or None, instance=dataset)
    form.fields["organisation"].queryset = request.user.organisations.all()

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_licence',[obj.name])

    return render(request, "datasets/edit_organisation.html", {
        'form': form,
        'dataset': dataset,
        'organisations': organisations,
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_licence(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    form = f.LicenceForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_location', [obj.name])

    return render(request, "datasets/edit_licence.html", {
        'form': form,
        'dataset': dataset,
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_location(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    form = f.LocationForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_frequency', [obj.name])

    return render(request, "datasets/edit_location.html", {
        'form': form,
        'dataset': dataset,
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_frequency(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    form = f.FrequencyForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            url = _frequency_redirect_to(obj)

            return _redirect_to(request, url, [obj.name])


    return render(request, "datasets/edit_frequency.html", {
        'form': form,
        'dataset': dataset,
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_addfile(request, dataset_name, datafile_id=None):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.FileForm(request.POST or None, instance=datafile)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                data['dataset'] = dataset
                obj = Datafile.objects.create(**data)
                obj.save()

            return _return_to(request, 'edit_dataset_files', [dataset_name])

    return render(request, "datasets/edit_addfile.html", {
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_deletefile(request, dataset_name, datafile_id):
    datafile = get_object_or_404(Datafile, id=datafile_id)

    if not user_can_edit_datafile(request.user, datafile):
        return HttpResponseForbidden()

    datafile.delete();

    return _return_to(request, 'edit_dataset_files', [dataset_name])


def edit_addfile_weekly(request, dataset_name, datafile_id=None):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.WeeklyFileForm(request.POST or None, instance=datafile)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                data['dataset'] = dataset
                obj = Datafile.objects.create(**data)
                obj.save()

            return _return_to(request, 'edit_dataset_files', [dataset_name])



    return render(request, "datasets/edit_addfile_week.html", {
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_addfile_monthly(request, dataset_name, datafile_id=None):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.MonthlyFileForm(request.POST or None, instance=datafile)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''


    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()


    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                data['dataset'] = dataset
                obj = Datafile.objects.create(**data)
                obj.save()

            return _return_to(request, 'edit_dataset_files', [dataset_name])

    return render(request, "datasets/edit_addfile_month.html", {
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
        'return_to': return_to,
        'return_to_qs' : return_to_qs
    })


def edit_addfile_quarterly(request, dataset_name, datafile_id=None):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.QuarterlyFileForm(request.POST or None, instance=datafile)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                data['dataset'] = dataset
                obj = Datafile.objects.create(**data)
                obj.save()

            return _return_to(request, 'edit_dataset_files', [dataset_name])


    return render(request, "datasets/edit_addfile_quarter.html", {
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_addfile_annually(request, dataset_name, datafile_id = None):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.AnnuallyFileForm(request.POST or None, instance=datafile)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                data['dataset'] = dataset
                obj = Datafile.objects.create(**data)
                obj.save()

            return _return_to(request, 'edit_dataset_files', [dataset_name])



    return render(request, "datasets/edit_addfile_year.html", {
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_files(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    url = _frequency_redirect_to(dataset)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    return render(request, "datasets/show_files.html", {
        'addfile_viewname': url,
        'dataset': dataset,
        'return_to': return_to,
        'return_to_qs' : return_to_qs
    })


def edit_add_doc(request, dataset_name, datafile_id=None):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.FileForm(request.POST or None)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                data['dataset'] = dataset
                data['is_documentation'] = True
                obj = Datafile.objects.create(**data)
                obj.save()

            return _return_to(request, 'edit_dataset_documents', [dataset_name])

    return render(request, "datasets/edit_adddoc.html", {
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
        'return_to': return_to,
        'return_to_qs': return_to_qs
    })


def edit_documents(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    return render(request, "datasets/show_docs.html", {
        'dataset': dataset,
        'return_to': return_to,
        'return_to_qs' : return_to_qs
    })


def edit_notifications(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    return_to = request.GET.get('return_to', '')
    return_to_qs = ('?return_to=' + return_to) if return_to else ''

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if dataset.frequency in ['daily', 'never']:
        dataset.notifications = 'no'
        dataset.save()

        return _redirect_to(
            request,
            'edit_dataset_check_dataset',
            [dataset.name]
        )

    form = f.NotificationsForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(
                request,
                'edit_dataset_check_dataset',
                [obj.name]
            )

    return render(request, "datasets/edit_notifications.html", {
        'form': form,
        'dataset': dataset,
        'return_to': return_to,
        'return_to_qs' : return_to_qs
    })


def check_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    organisation = dataset.organisation
    organisations = organisations_for_user(request.user)
    single_organisation = len(organisations) == 1

    if request.method == 'POST':
        dataset.published = True
        dataset.published_date = datetime.now()
        dataset.save()

        err = publish_to_ckan(dataset)
        index_dataset(dataset)

        return HttpResponseRedirect(
            reverse('manage_data') + '?result=created'
        )

    datafiles = dataset.files.filter(is_documentation=False).all()
    docfiles = dataset.files.filter(is_documentation=True).all()

    return render(request, "datasets/check_dataset.html", {
        'dataset': dataset,
        'licence': dataset.licence if dataset.licence != 'other' else dataset.licence_other,
        'organisation': organisation,
        'single_organisation': single_organisation,
        'docfiles': docfiles,
        'datafiles': datafiles
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
    if request.POST.get('return_to') == "check":
        return HttpResponseRedirect(
            reverse('edit_dataset_check_dataset', args=args)
        )

    return HttpResponseRedirect(
        reverse(url_name, args=args)
    )

def _qsp_return_to(value):
    return '?return_to=' + value if value else ''

def _return_to(request, url_name, args):
    ret = request.POST.get('return_to')
    return HttpResponseRedirect(
        reverse(url_name, args=args) + _qsp_return_to(ret)
    )
