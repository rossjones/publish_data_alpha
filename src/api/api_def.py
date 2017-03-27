from django.conf.urls import url, include
from datasets.models import Dataset, Organisation, Datafile
from rest_framework import serializers, viewsets

class DatafileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Datafile
        exclude = ('month', 'year', 'quarter', 'dataset')

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organisation
        exclude = ('users',)
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    organisation = OrganisationSerializer(many=False, read_only=True)
    files = DatafileSerializer(many=True, read_only=False)

    class Meta:
        model = Dataset
        exclude = ('owner', 'creator', 'legacy_metadata')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    lookup_field = 'name'

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    lookup_field = 'name'
