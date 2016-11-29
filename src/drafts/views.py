from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.urls import reverse

import drafts.forms as f
from drafts.models import Dataset, Datafile
from drafts.util import convert_to_slug

FORMS = {
    # Maps from the form name to the actual form
    'title': f.NewDatasetForm,
    'licence': f.LicenceForm,
    'theme':   f.ThemeForm,
    'country': f.CountryForm,
    'frequency': f.FrequencyForm,
    'notifications': f.NotificationsForm
}

NEXT_STEP = {
    # Maps from form name, to the name of the next url to redirect to
    'licence': 'edit_theme',
    'theme': 'edit_country',
    'country': 'edit_frequency',
    'frequency': 'edit_addfile',
    'notifications': 'check_dataset'
}

def new_dataset(request):

    form = f.NewDatasetForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            name = convert_to_slug(form.cleaned_data['title'])

            Dataset.objects.create(name=name,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'])

            return redirect(reverse('edit_licence', args=[name]))

    return render(request, "drafts/edit_title.html", {
        "form": form,
    })

def edit_dataset(request, dataset_name, form_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = FORMS.get(form_name)(request.POST or dataset.as_dict())

    if request.method == "POST":
        if form.is_valid():

            form.update_model(dataset)
            dataset.save()

            return redirect(
                reverse('{}'.format(NEXT_STEP.get(form_name)),
                        args=[dataset_name])
            )

    return render(request, "drafts/edit_{}.html".format(form_name), {
        "dataset": dataset,
        "form": form,
    })

def add_file(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    form = f.AddFileForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            Datafile.objects.create(
                title=form.cleaned_data['title'],
                url=form.cleaned_data['url'],
                dataset=dataset
            )


            return redirect(
                reverse('show_files',
                        args=[dataset_name])
            )

    return render(request, "drafts/edit_addfile.html", {
        "dataset": dataset,
        "form": form,
    })

def show_files(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    return render(request, "drafts/show_files.html", {
        "dataset": dataset,
    })

def check_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    return render(request, "drafts/check_dataset.html", {
        "dataset": dataset,
    })
