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
        max_length=8096,
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
        max_length=8096,
        widget=forms.Textarea,
        required=False
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

    def __init__(self, datafile_count=None, data=None):
        super(PublishForm, self ).__init__(data)
        self.datafile_count = datafile_count

    def clean(self):
        if self.datafile_count == 0:
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

    frequency = forms.CharField(required=True)

    class Meta:
        model = Dataset
        fields = ['frequency']


class CheckedFileForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        error_messages={'required': 'Please enter a valid name'}
    )
    url = forms.CharField(
        required=True,
        error_messages={'required': 'Please enter a valid URL'}
    )
    is_broken = forms.BooleanField(required=False)

    def clean(self):
        cleaned = super(CheckedFileForm, self).clean()
        if self._errors:
            return cleaned

        # Check the URL is a valid URL and exists
        exists, fmt, size, error_msg = url_exists(cleaned['url'])
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
        cleaned['size'] = size

        return cleaned


class FileForm(CheckedFileForm):

    class Meta:
        model = Datafile
        fields = [ 'name', 'url' ]


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
            'name', 'url',
            'start_day', 'start_month', 'start_year',
            'end_day', 'end_month', 'end_year'
        ]

    def clean(self):
        cleaned = CheckedFileForm.clean(self)

        if not 'start_year' in cleaned or \
            cleaned['start_year'] < 1000 or cleaned['start_year'] > 3000:
            self._errors['start_year'] = \
                [_('Please enter a correct year')]
        elif not 'start_month' in cleaned or \
            cleaned['start_month'] < 1 or cleaned['start_month'] > 12:
            self._errors['start_month'] = \
                [_('Please enter a correct month')]
        elif not 'start_day' in cleaned or \
            cleaned['start_day'] < 1 or cleaned['start_day'] > 31:
            self._errors['start_day'] = \
                [_('Please enter a correct day')]
        else:
            try:
                frequency_weekly_start = datetime.date(
                    cleaned['start_year'],
                    cleaned['start_month'],
                    cleaned['start_day']
                )
            except (KeyError, ValueError):
                self._errors['start_date'] = \
                    [_('Please enter a correct start date')]

        if not 'end_year' in cleaned or \
            cleaned['end_year'] < 1000 or cleaned['end_year'] > 3000:
            self._errors['end_year'] = \
                [_('Please enter a correct year')]
        elif not 'end_month' in cleaned or \
            cleaned['end_month'] < 1 or cleaned['end_month'] > 12:
            self._errors['end_month'] = \
                [_('Please enter a correct month')]
        elif not 'end_day' in cleaned or \
            cleaned['end_day'] < 1 or cleaned['end_day'] > 31:
            self._errors['end_day'] = \
                [_('Please enter a correct day')]
        else:
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


        return {
            'is_broken': False,
            'last_check': datetime.datetime.now(),
            'size': cleaned['size'],
            'name': cleaned['name'],
            'url': cleaned['url'],
            'start_date': frequency_weekly_start,
            'end_date': frequency_weekly_end
        }


class MonthlyFileForm(CheckedFileForm):

    month = forms.IntegerField(
        required=True,
        error_messages={'required': 'Please enter a valid month'}
    )

    year = forms.IntegerField(
        required=True,
        error_messages={'required': 'Please enter a valid year'}
    )


    class Meta:
        frequency = 'monthly'
        model = Datafile
        fields = [ 'name', 'url', 'month', 'year' ]


    def clean(self):
        cleaned = CheckedFileForm.clean(self)
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

        print(cleaned)
        return cleaned


class QuarterlyFileForm(CheckedFileForm):
    quarter = forms.IntegerField(
        required=True,
        error_messages={'required': 'Please select a quarter'}
    )

    class Meta:
        frequency = 'quarterly'
        model = Datafile
        fields = [ 'name', 'url', 'quarter', 'year' ]

    def clean(self):
        cleaned = CheckedFileForm.clean(self)

        if not cleaned['year'] or \
           cleaned['year'] < 1000 or \
           cleaned['year'] > 3000:
            self._errors['year'] = [_('Please enter a valid year')]

        return cleaned


class AnnuallyFileForm(CheckedFileForm):

    year = forms.IntegerField(
        required=True,
        error_messages={'required': 'Please enter a valid year'}
    )

    class Meta:
        frequency = 'annually'
        model = Datafile
        fields = [ 'name', 'url', 'year' ]

    def clean(self):
        cleaned = CheckedFileForm.clean(self)
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



class DateForm(forms.Form):
    start_date = forms.CharField(required=False)
    end_date = forms.CharField(required=False)
