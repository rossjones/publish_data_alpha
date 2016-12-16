from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import drafts.forms as f
from drafts.models import Dataset, Datafile
from django.views.generic.edit import FormView
from formtools.wizard.views import NamedUrlSessionWizardView
from ckan_proxy.logic import organization_show

from userauth.logic import get_orgs_for_user

FORMS = (
    ('organisation', f.OrganisationForm),
    ('licence', f.LicenceForm),
    ('country', f.CountryForm),
    ('frequency', f.FrequencyForm),

    # These are used conditionally
    ('frequency_weekly', f.FrequencyWeeklyForm),
    ('frequency_monthly', f.FrequencyMonthlyForm),
    ('frequency_quarterly', f.FrequencyQuarterlyForm),
    ('frequency_annually', f.FrequencyAnnuallyForm),

    ('add_file', f.AddFileForm),
    ('files', f.StubForm),
    ('notifications', f.NotificationsForm),
    ('check_dataset', f.StubForm),
)

TEMPLATES = {
    'organisation': 'drafts/edit_organisation.html',
    'licence': 'drafts/edit_licence.html',
    'country': 'drafts/edit_country.html',
    'frequency': 'drafts/edit_frequency.html',
    'frequency_weekly': 'drafts/edit_frequency_week.html',
    'frequency_monthly': 'drafts/edit_frequency_month.html',
    'frequency_quarterly': 'drafts/edit_frequency_quarter.html',
    'frequency_annually': 'drafts/edit_frequency_year.html',
    'add_file': 'drafts/edit_addfile.html',
    'files': 'drafts/show_files.html',
    'notifications': 'drafts/edit_notifications.html',
    'check_dataset': 'drafts/check_dataset.html'
}


class DatasetEdit(FormView):
    model = Dataset
    form_class = f.DatasetForm
    template_name = 'drafts/edit_title.html'

class DatasetCreate(FormView):
    model = Dataset
    form_class = f.DatasetForm
    template_name = 'drafts/edit_title.html'

    def form_valid(self, form):
        dataset = Dataset.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
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


        return reverse('edit_dataset_step', kwargs={
            'dataset_name': self.object.name,
            'step': 'organisation'
        })

        # Only one organisation
        #return reverse('edit_dataset_step', kwargs={
        #    'dataset_name': self.object.name,
        #    'step': 'licence'
        #})

class DatasetWizard(NamedUrlSessionWizardView):

    instance = None

    def dispatch(self, request, *args, **kwargs):
        if 'dataset_name' in kwargs:
            self.instance = get_object_or_404(Dataset, name=kwargs['dataset_name'])

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
        context = super(DatasetWizard, self).get_context_data(form=form, **kwargs)
        if self.instance:
            context['dataset'] = self.instance

        if kwargs.get('step') == 'check_dataset':
            org = organization_show(self.instance.organisation) or {}
            context['organisation_title'] = org.get('title')

        context['organisations'] = get_orgs_for_user(self.request)
        return context

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        if self.instance:
            initial.update(self.instance.as_dict())
        return initial

    def get_form_kwargs(self, step):
        if step == 'add_file':
            return {'instance': Datafile()}
        return {'instance': self.instance}

    def process_step(self, form):
        if self.steps.current == 'add_file':
            model = form.save(commit=False)
            model.dataset = self.instance
            model.save()
        else:
            form.save()

        return self.get_form_step_data(form)

    def done(self, form_list, **kwargs):
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
