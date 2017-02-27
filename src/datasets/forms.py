from django.utils.translation import ugettext as _
from django import forms
import datetime

from datasets.models import Dataset, Datafile
from datasets.util import url_exists


class DatasetForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=100, required=True)
    summary = forms.CharField(label=_('Summary'), max_length=200, required=True)
    description = forms.CharField(
        label=_('Additional Information'),
        max_length=1024,
        widget=forms.Textarea,
        required=False
    )

    def clean(self):
        if 'title' in self.cleaned_data:
            title = self.cleaned_data['title']
            length = len(list(filter(lambda x: x.isalpha(), title)))
            if length < 3:
                self._errors['title'] = [_('This title is not valid')]
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


class PublishForm(forms.Form):
    '''
    Used to verify that the required fields are present in the
    dataset. As the models themselves don't enforce that fields
    are required, we will set them as required in the constructor.
    '''

    title = forms.CharField(required=True)
    summary = forms.CharField(required=True)
    description = forms.CharField(required=False)
    licence = forms.CharField(required=True)
    organisation = forms.CharField(required=True)
    frequency = forms.CharField(required=True)
    files = forms.CharField(required=False)

    def __init__(self, file_count=None, data=None):
        super(PublishForm, self ).__init__(data)
        self.file_count = file_count

    def clean(self):
        if self.file_count == 0:
            self._errors['files'] = [_('You must add at least one link')]

        if 'title' in self.cleaned_data:
            title = self.cleaned_data['title']
            length = len(list(filter(lambda x: x.isalpha(), title)))
            if length < 3:
                self._errors['title'] = [_('This title is not valid')]

        if 'licence' in self.cleaned_data:
            if self.cleaned_data['licence'] == 'other' \
                    and not self.cleaned_data.get('licence_other'):
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
                    and not self.cleaned_data.get('licence_other'):
                self._errors['licence_other'] = \
                    [_('Please type the name of your licence')]
        return self.cleaned_data


class LocationForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['location1', 'location2', 'location3' ]


class OrganisationForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['organisation']


class FrequencyForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['frequency']


class CheckedFileForm(forms.ModelForm):

    title = forms.CharField(required=True)
    url = forms.CharField(required=True)
    is_broken = forms.BooleanField(required=False)

    def clean(self):
        cleaned = super(CheckedFileForm, self).clean()
        if self._errors:
            return cleaned

        # Check the URL is a valid URL and exists
        exists, fmt, error_msg = url_exists(cleaned['url'])
        if not exists:
            self._errors['url'] = \
                [error_msg]

            # TODO: Consider uncommenting this
            #if fmt == 'HTML':
            #    self._errors['url'] = \
            #        [_("This appears to be a web page and not a data file")]

        cleaned['is_broken'] = False
        cleaned['last_check'] = datetime.datetime.now()
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
        cleaned = super(CheckedFileForm, self).clean()
        if self._errors:
            return cleaned

        try:
            frequency_weekly_start = datetime.date(
                cleaned['start_year'],
                cleaned['start_month'],
                cleaned['start_day']
            )
        except (KeyError, ValueError):
            self._errors['start_date'] = \
                [_('Please enter a correct start date')]

        try:
            frequency_weekly_end = datetime.date(
                cleaned['end_year'],
                cleaned['end_month'],
                cleaned['end_day']
            )
        except (KeyError, ValueError):
            self._errors['end_date'] = \
                [_('Please enter a correct end date')]

        if self.errors:
            return cleaned

        # Check the URL is a valid URL and exists
        exists, fmt, error_msg = url_exists(cleaned['url'])
        if not exists:
            self._errors['url'] = \
                [error_msg]

            # TODO: Consider uncommenting this
            #if fmt == 'HTML':
            #    self._errors['url'] = \
            #        [_("This appears to be a web page and not a data file")]

        return {
            'is_broken': False,
            'last_check': datetime.datetime.now(),
            'format': fmt,
            'title': cleaned['title'],
            'url': cleaned['url'],
            'start_date': frequency_weekly_start,
            'end_date': frequency_weekly_end
        }


class MonthlyFileForm(CheckedFileForm):

    class Meta:
        frequency = 'monthly'
        model = Datafile
        fields = [ 'title', 'url', 'month', 'year' ]


    def clean(self):
        cleaned = super(CheckedFileForm, self).clean()
        if self._errors:
            return cleaned

        try:
            date = datetime.date(
                cleaned['year'],
                cleaned['month'],
                1
            )
        except (KeyError, ValueError):
            self._errors['date'] = [_('Please enter a valid date')]

        return cleaned


class QuarterlyFileForm(CheckedFileForm):

    class Meta:
        frequency = 'quarterly'
        model = Datafile
        fields = [ 'title', 'url', 'quarter', 'year' ]


class AnnuallyFileForm(CheckedFileForm):

    class Meta:
        frequency = 'annually'
        model = Datafile
        fields = [ 'title', 'url', 'year' ]

    def clean(self):
        cleaned = super(CheckedFileForm, self).clean()
        if self._errors:
            return cleaned

        if cleaned['year'] < 1000 or cleaned['year'] > 3000:
            self._errors['year'] = [_('Please enter a valid year')]

        return cleaned



class StubForm(forms.ModelForm):
    """ This is a do-nothing form for handling a page
        that has no form """

    class Meta:
        model = Datafile
        fields = []


class NotificationsForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['notifications']


class DateForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
