from django.utils.translation import ugettext as _
from django import forms
import datetime

import datasets.choices as choices
from datasets.models import Dataset, Datafile
from datasets.util import convert_to_slug, url_exists


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


class EditDatasetForm(forms.ModelForm):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    summary = forms.CharField(label=_('Summary'), max_length=200, required=True)
    description = forms.CharField(
        label=_('Additional Information'),
        max_length=1024,
        widget=forms.Textarea,
        required=True
    )

    class Meta:
        model = Dataset
        fields = ['title', 'summary', 'description']



class FullDatasetForm(forms.ModelForm):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    summary = forms.CharField(label=_('Summary'), max_length=200, required=True)
    description = forms.CharField(
        label=_('Additional Information'),
        max_length=1024,
        widget=forms.Textarea,
        required=True
    )

    class Meta:
        model = Dataset
        fields = [
            'title', 'summary', 'description',
            'licence', 'licence_other', 'organisation',
            'frequency', 'notifications', 'name'
        ]


    def clean(self):
        if 'licence' in self.cleaned_data:
            if self.cleaned_data['licence'] == 'other' \
                    and not self.cleaned_data['licence_other']:
                self._errors['licence_other'] = \
                    [_('Please type the name of your licence')]

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


class LocationForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['location']


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

class CheckedFileForm(forms.ModelForm):

    title = forms.CharField(required=True)
    url = forms.CharField(required=True)

    def clean(self):
        cleaned = super(CheckedFileForm, self).clean()
        if self._errors:
            return cleaned

        # Check the URL is a valid URL and exists
        exists, fmt = url_exists(cleaned['url'])
        if not exists:
            self._errors['url'] = \
                [_("This URL can't be reached")]

            # TODO: Consider uncommenting this
            #if fmt == 'HTML':
            #    self._errors['url'] = \
            #        [_("This appears to be a web page and not a data file")]

        cleaned['format'] = fmt

        return cleaned


class FileForm(CheckedFileForm):

    class Meta:
        model = Datafile
        fields = [ 'title', 'url' ]


class WeeklyFileForm(CheckedFileForm):

    start_day = forms.IntegerField(required=True)
    start_month = forms.IntegerField(required=True)
    start_year = forms.IntegerField(required=True)
    end_day = forms.IntegerField(required=True)
    end_month = forms.IntegerField(required=True)
    end_year = forms.IntegerField(required=True)

    class Meta:
        frequency = 'weekly'
        model = Datafile
        fields = [
            'title', 'url',
            'start_day', 'start_month', 'start_year',
            'end_day', 'end_month', 'end_year'
        ]

    def clean(self):
        try:
            frequency_weekly_start = datetime.date(
                self.cleaned_data['start_year'],
                self.cleaned_data['start_month'],
                self.cleaned_data['start_day']
            )
        except (KeyError, ValueError):
            self._errors['start_date'] = \
                [_('Please enter a correct start date')]

        try:
            frequency_weekly_end = datetime.date(
                self.cleaned_data['end_year'],
                self.cleaned_data['end_month'],
                self.cleaned_data['end_day']
            )
        except (KeyError, ValueError):
            self._errors['end_date'] = \
                [_('Please enter a correct end date')]

        if self.errors:
            return self.cleaned_data

        return {
            'title': self.cleaned_data['title'],
            'url': self.cleaned_data['url'],
            'start_date': frequency_weekly_start,
            'end_date': frequency_weekly_end
        }



class MonthlyFileForm(CheckedFileForm):

    class Meta:
        frequency = 'monthly'
        model = Datafile
        fields = [ 'title', 'url', 'month', 'year' ]


class QuarterlyFileForm(CheckedFileForm):

    class Meta:
        frequency = 'quarterly'
        model = Datafile
        fields = [ 'title', 'url', 'quarter' ]


class AnnuallyFileForm(CheckedFileForm):

    class Meta:
        frequency = 'annually'
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
