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

class LicenceForm(forms.Form):
    licence = forms.ChoiceField(widget=forms.RadioSelect, choices=choices.LICENCE_CHOICES)
    licence_other = forms.CharField(
        label=_('Other'),
        max_length=1024,
        required=False
    )

class ThemeForm(forms.Form):
    theme = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=choices.THEME_CHOICES,
    )

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

class FrequencyForm(forms.Form):
    frequency = forms.ChoiceField(widget=forms.RadioSelect, choices=choices.FREQUENCY_CHOICES)

class AddFileForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    url = forms.URLField(label=_('URL'), max_length=100, required=True)

