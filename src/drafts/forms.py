from django.utils.translation import ugettext as _
from django import forms

import drafts.choices as choices
from drafts.models import Dataset
from drafts.util import convert_to_slug

class DatasetForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    description = forms.CharField(
        label=_('Description'),
        max_length=1024,
        widget=forms.Textarea,
        required=True
    )

    def clean(self):
        name = convert_to_slug(self.cleaned_data['title'])
        if not name:
            self._errors["password"] = [_("Title is not valid")]
        self.cleaned_data["name"] = name
        return self.cleaned_data



class CountryForm(forms.Form):
    countries = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=choices.COUNTRY_CHOICES,
    )


class LicenceForm(forms.Form):
    licence = forms.ChoiceField(widget=forms.RadioSelect, choices=choices.LICENCE_CHOICES)
    licence_other = forms.CharField(
        label=_('Other'),
        max_length=1024,
        required=False
    )


class FrequencyForm(forms.Form):
    frequency = forms.ChoiceField(widget=forms.RadioSelect, choices=choices.FREQUENCY_CHOICES)


class AddFileForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    url = forms.URLField(label=_('URL'), max_length=100, required=True)


class NotificationsForm(forms.Form):
    notifications = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(('yes', 'Yes'),('no', 'No')))

class DateForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
