from django.utils.translation import ugettext as _
from django import forms

import drafts.choices as choices


class NewDatasetForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    description = forms.CharField(
        label=_('Description'),
        max_length=1024,
        widget=forms.Textarea,
        required=True
    )

    def update_model(self, dataset):
        dataset.title = self.cleaned_data['title']
        dataset.description = self.cleaned_data['description']


class LicenceForm(forms.Form):
    licence = forms.ChoiceField(widget=forms.RadioSelect, choices=choices.LICENCE_CHOICES)
    licence_other = forms.CharField(
        label=_('Other'),
        max_length=1024,
        required=False
    )

    def update_model(self, dataset):
        dataset.licence = self.cleaned_data['licence']
        dataset.licence_other = self.cleaned_data['licence_other']


class CountryForm(forms.Form):
    countries = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=choices.COUNTRY_CHOICES,
    )
    country_other = forms.CharField(
        label=_('Other'),
        max_length=1024,
        required=False
    )

    def update_model(self, dataset):
        dataset.countries = self.cleaned_data['countries']
        dataset.countries_other = self.cleaned_data['country_other']


class FrequencyForm(forms.Form):
    frequency = forms.ChoiceField(widget=forms.RadioSelect, choices=choices.FREQUENCY_CHOICES)

    def update_model(self, dataset):
        dataset.frequency = self.cleaned_data['frequency']


class AddFileForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    url = forms.URLField(label=_('URL'), max_length=100, required=True)

    def update_model(self, dataset):
        pass


class NotificationsForm(forms.Form):
    notifications = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(('yes', 'Yes'),('no', 'No')))

    def update_model(self, dataset):
        dataset.notifications = self.cleaned_data['notifications']
