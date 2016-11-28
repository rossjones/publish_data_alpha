from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.urls import reverse

import drafts.forms as f

FORMS = {
    'title': f.NewDatasetForm,
    'licence': f.LicenceForm,
    'theme':   f.ThemeForm,
}

NEXT_STEP = {
    'licence': 'edit_theme',
    'theme': ''
}

def new_dataset(request):

    form = f.NewDatasetForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # We must check whether it is in use ....
            name = slugify(form.cleaned_data['title'])
            return redirect(reverse('edit_licence', args=[name]))

    return render(request, "drafts/edit_title.html", {
        "form": form,
    })

def edit_dataset(request, dataset_name, form_name):
    form = FORMS.get(form_name)(request.POST or None)
    if request.method == "POST":
        if form.is_valid():

            return redirect(
                reverse('{}'.format(NEXT_STEP.get(form_name)),
                        args=[dataset_name])
            )

    return render(request, "drafts/edit_{}.html".format(form_name), {
        "dataset_name": dataset_name,
        "form": form,
    })

