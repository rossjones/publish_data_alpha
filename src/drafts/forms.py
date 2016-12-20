from django.utils.translation import ugettext as _
from django import forms
import datetime

import drafts.choices as choices
from drafts.models import Dataset, Datafile
from drafts.util import convert_to_slug


class DatasetForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    summary = forms.CharField(label=_('Summary'), max_length=200, required=True)
    description = forms.CharField(
        label=_('Additional Information'),
        max_length=1024,
        widget=forms.Textarea,
        required=True
    )

    def clean(self):
        if 'title' in self.cleaned_data:
            name = convert_to_slug(self.cleaned_data['title'])
            if not name:
                self._errors['title'] = [_('This title is not valid')]
            self.cleaned_data['name'] = name
        return self.cleaned_data


class LicenceForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['licence', 'licence_other']

    def clean(self):
        if 'licence' in self.cleaned_data:
            if self.cleaned_data['licence'] == 'other' \
                    and not self.cleaned_data['licence_other']:
                self._errors['licence_other'] = \
                    [_('Please type the name of your licence')]
        return self.cleaned_data


class CountryForm(forms.ModelForm):

    countries = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=choices.COUNTRY_CHOICES,
    )

    class Meta:
        model = Dataset
        fields = ['countries']


class OrganisationForm(forms.ModelForm):

    organisation = forms.CharField(required=True)

    class Meta:
        model = Dataset
        fields = ['organisation']


class FrequencyForm(forms.ModelForm):

    frequency = forms.CharField(required=True)

    class Meta:
        model = Dataset
        fields = ['frequency']


class FileForm(forms.ModelForm):

    class Meta:
        model = Datafile
        fields = [ 'title', 'url' ]


class WeeklyFileForm(forms.ModelForm):

    start_day = forms.IntegerField(required=True)
    start_month = forms.IntegerField(required=True)
    start_year = forms.IntegerField(required=True)
    end_day = forms.IntegerField(required=True)
    end_month = forms.IntegerField(required=True)
    end_year = forms.IntegerField(required=True)

    class Meta:
        model = Datafile
        fields = [
            'title', 'url',
            'start_day', 'start_month', 'start_year',
            'end_day', 'end_month', 'end_year'
        ]

    def clean(self):
        try:
            self.cleaned_data['frequency_weekly_start'] = datetime.date(
                self.cleaned_data['start_year'],
                self.cleaned_data['start_month'],
                self.cleaned_data['start_day']
            )
        except (KeyError, ValueError):
            self._errors['start_date'] = \
                [_('Please enter a correct start date')]

        try:
            self.cleaned_data['frequency_weekly_end'] = datetime.date(
                self.cleaned_data['end_year'],
                self.cleaned_data['end_month'],
                self.cleaned_data['end_day']
            )
        except (KeyError, ValueError):
            self._errors['end_date'] = \
                [_('Please enter a correct end date')]

        return self.cleaned_data


class MonthlyFileForm(forms.ModelForm):

    class Meta:
        model = Datafile
        fields = [ 'title', 'url', 'month', 'year' ]


class QuarterlyFileForm(forms.ModelForm):

    class Meta:
        model = Datafile
        fields = [ 'title', 'url', 'quarter' ]


class AnnuallyFileForm(forms.ModelForm):

    class Meta:
        model = Datafile
        fields = [ 'title', 'url', 'year' ]


class StubForm(forms.ModelForm):
    """ This is a do-nothing form for handling a page
        that has no form """

    class Meta:
        model = Datafile
        fields = []


class NotificationsForm(forms.ModelForm):

    notifications = forms.CharField(required=True)

    class Meta:
        model = Dataset
        fields = ['notifications']


class DateForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
