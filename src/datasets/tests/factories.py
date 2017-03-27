import factory
from factory.django import DjangoModelFactory


from django.contrib.auth import get_user_model

class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = 'datasets.organisation'
        django_get_or_create = ('name',)

    name='test-org'
    title='Test Organisation',
    description='Test Organisation Description'


class DatasetFactory(DjangoModelFactory):
    class Meta:
        model = 'datasets.dataset'
        django_get_or_create = ('name',)

    name = 'a-test-dataset'
    title = 'A test dataset'
    summary = 'A test summary'
    frequency = 'weekly'
    organisation_id = ''

class DatafileFactory(DjangoModelFactory):
    class Meta:
        model = 'datasets.datafile'
        django_get_or_create = ('url', 'dataset')

    name = 'A test file'
    url = 'https://data.gov.uk'
    format = 'HTML'
    dataset = None


class GoodUserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = 'test-safe-user'
    email = 'test-safe-user@localhost'
    password = 'password'


class NaughtyUserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username="Naughty Test User Signin",
    email="naughty-user@localhost",
