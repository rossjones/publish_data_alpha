from django.conf.urls import url, include

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend

from datasets.models import Dataset, Organisation, Datafile
from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

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

    def create(self, validated_data):
        resources = validated_data.pop('files')
        dataset = Dataset.objects.create(**validated_data)
        for r in resources:
            r['dataset_id'] = dataset.id
            Datafile.objects.create(**r)

        return dataset


class DatasetList(generics.ListCreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    lookup_field = 'name'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'title',)
    permission_classes = (IsAuthenticatedOrReadOnly, )

class OrganisationList(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    lookup_field = 'name'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'title',)
    permission_classes = (IsAuthenticatedOrReadOnly, )


class DatasetDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'name'
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = (IsAdminOrReadOnly, )


class OrganisationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'name'
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = (IsAdminOrReadOnly, )
