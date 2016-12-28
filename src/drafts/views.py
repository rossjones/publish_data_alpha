
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect


import drafts.forms as f
from userauth.logic import get_orgs_for_user
from drafts.models import Dataset, Datafile
from ckan_proxy.convert import draft_to_ckan
from ckan_proxy.logic import (organization_show,
                              dataset_show,
                              dataset_create,
                              dataset_update)

from formtools.wizard.views import NamedUrlSessionWizardView

FORMS = (
    ('organisation', f.OrganisationForm),
    ('licence', f.LicenceForm),
    ('country', f.CountryForm),
    ('frequency', f.FrequencyForm),

    # These are used conditionally
    ('addfile_weekly', f.WeeklyFileForm),
    ('addfile_monthly', f.MonthlyFileForm),
    ('addfile_quarterly', f.QuarterlyFileForm),
    ('addfile_annually', f.AnnuallyFileForm),
    ('addfile_daily', f.FileForm),
    ('addfile_never', f.FileForm),

    ('files', f.StubForm),
    ('notifications', f.NotificationsForm),
    ('check_dataset', f.StubForm),
)

TEMPLATES = {
    'organisation': 'drafts/edit_organisation.html',
    'licence': 'drafts/edit_licence.html',
    'country': 'drafts/edit_country.html',
    'frequency': 'drafts/edit_frequency.html',
    'addfile_daily': 'drafts/edit_addfile.html',
    'addfile_never': 'drafts/edit_addfile.html',
    'addfile_weekly': 'drafts/edit_addfile_week.html',
    'addfile_monthly': 'drafts/edit_addfile_month.html',
    'addfile_quarterly': 'drafts/edit_addfile_quarter.html',
    'addfile_annually': 'drafts/edit_addfile_year.html',
    'files': 'drafts/show_files.html',
    'notifications': 'drafts/edit_notifications.html',
    'check_dataset': 'drafts/check_dataset.html'
}


class DatasetEdit(FormView):
    model = Dataset
    form_class = f.DatasetForm
    template_name = 'drafts/edit_title.html'

    def get_initial(self):
        if 'dataset_name' in self.kwargs:
            self.instance = get_object_or_404(
                Dataset,
                name=self.kwargs['dataset_name']
            )
            return self.instance.as_dict()
        return {}

    def get_context_data(self, **kwargs):
        context = super(DatasetEdit, self).get_context_data(**kwargs)
        context['target_url'] = reverse('edit_dataset', args=[self.instance.name])
        return context

    def form_valid(self, form):
        self.instance.title=form.cleaned_data['title']
        self.instance.description=form.cleaned_data['description']
        self.instance.summary=form.cleaned_data['summary']
        self.instance.save()
        return super(DatasetEdit, self).form_valid(form)


    def get_success_url(self):
        return reverse(
            'edit_dataset_step',
            args=[self.instance.name, 'check_dataset']
        )


class DatasetCreate(FormView):
    model = Dataset
    form_class = f.DatasetForm
    template_name = 'drafts/edit_title.html'

    def form_valid(self, form):
        dataset = Dataset.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                summary=form.cleaned_data['summary'],
                creator=self.request.user,
                name=form.cleaned_data['name']
        )
        self.object = dataset
        return super(DatasetCreate, self).form_valid(form)

    def get_initial(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(DatasetCreate, self).get_context_data(**kwargs)
        context['target_url'] = reverse('new_dataset')
        return context

    def get_success_url(self):
        if 'wizard_dataset_wizard' in self.request.session:
            del self.request.session['wizard_dataset_wizard']

        return reverse('edit_dataset_step', kwargs={
            'dataset_name': self.object.name,
            'step': 'organisation'
        })

        # Only one organisation
        # return reverse('edit_dataset_step', kwargs={
        #    'dataset_name': self.object.name,
        #    'step': 'licence'
        # })

class DatasetWizard(NamedUrlSessionWizardView):

    instance = None

    def dispatch(self, request, *args, **kwargs):
        if 'dataset_name' in kwargs:
            self.instance = get_object_or_404(
                Dataset,
                name=kwargs['dataset_name']
            )

        return super(DatasetWizard, self).dispatch(request, *args, **kwargs)

    def get_step_url(self, step):
        if step == "0":
            return reverse("new_dataset")

        return reverse(self.url_name, kwargs={
            'step': step,
            'dataset_name': self.instance.name
        })

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super(DatasetWizard, self).get_context_data(
            form=form, **kwargs
        )
        if self.instance:
            context['dataset'] = self.instance

        # Are we accessing this form because we got here from
        # the check_dataset page?
        context['editing'] = False
        if self.request.method == "GET" and self.request.GET.get('change'):
            context['editing'] = True

        if self.request.path.split('/')[-1] == 'check_dataset':
            org = organization_show(self.instance.organisation) or {}
            context['organisation_title'] = org.get('title')

        context['organisations'] = get_orgs_for_user(self.request)
        context['previous_step'] = self.steps.prev

        return context

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if self.instance:
            initial.update(self.instance.as_dict())
        return initial

    def get_form_kwargs(self, step):
        if step.startswith('addfile'):
            return {'instance': Datafile()}
        return {'instance': self.instance}

    def process_step(self, form):
        if self.steps.current.startswith('addfile'):
            model = form.save(commit=False)
            model.dataset = self.instance
            model.save()
        else:
            form.save()

        return self.get_form_step_data(form)

    def get(self, request, *args, **kwargs):
        self.storage.current_step = kwargs.get('step')
        return self.render(self.get_form())

    def post(self, *args, **kwargs):
        editing = self.request.POST.get('editing', "False")
        if editing == "True":
            # Save the current form if it is valid.
            form = self.get_form(data=self.request.POST, files=self.request.FILES)
            if form.is_valid():
                form.save()
            return self.render_goto_step("check_dataset")
        return super(DatasetWizard, self).post(*args, **kwargs)

    def done(self, form_list, **kwargs):
        f = dataset_update \
            if dataset_show(self.instance.name, self.request.user) \
            else dataset_create

        try:
            f(draft_to_ckan(self.instance), self.request.user)
        except Exception as e:
            # TODO: Handle the error correctly
            print(e)
        else:
            # Success! We can safely delete the draft now
            pass

        return HttpResponseRedirect('/manage?newset=1')


# Conditional processing of sub-forms for detail of frequency
def should_show_frequency_detail(wiz, expected):
    cleaned_data = wiz.get_cleaned_data_for_step('frequency') or {}
    return cleaned_data.get('frequency', '') == expected


def show_weekly_frequency(wizard):
    return should_show_frequency_detail(wizard, 'weekly')


def show_monthly_frequency(wizard):
    return should_show_frequency_detail(wizard, 'monthly')


def show_quarterly_frequency(wizard):
    return should_show_frequency_detail(wizard, 'quarterly')


def show_annually_frequency(wizard):
    return should_show_frequency_detail(wizard, 'annually')


def show_daily_frequency(wizard):
    return should_show_frequency_detail(wizard, 'daily')


def show_never_frequency(wizard):
    return should_show_frequency_detail(wizard, 'never')
