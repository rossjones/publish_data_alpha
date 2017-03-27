from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset, Datafile

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)

class DatafileDatesTestCase(TestCase):
    """ Test that when we save the start/end dates are set
    correctly in the datafile instance
    """

    def setUp(self):
        self.dataset = DatasetFactory.create()

    def skeleton(self):
        return Datafile(
            format='HTML',
            url='https://data.gov.uk',
            name='A datafile',
            dataset=self.dataset
        )

    def test_no_date(self):
        df = self.skeleton()
        df.save()

        assert df.start_date == None
        assert df.end_date == None

    def test_all_dates(self):
        df = self.skeleton()
        df.start_date = datetime(year=2017, month=1, day=1)
        df.end_date = datetime(year=2017, month=1, day=31)
        df.save()

        assert df.start_date == datetime(year=2017, month=1, day=1)
        assert df.end_date == datetime(year=2017, month=1, day=31)

    def test_year(self):
        df = self.skeleton()
        df.year = 2017
        df.save()

        assert df.start_date == datetime(year=2017, month=1, day=1)
        assert df.end_date == datetime(year=2017, month=12, day=31)

    def test_month(self):
        df = self.skeleton()
        df.month = 1
        df.year = 2017
        df.save()

        assert df.start_date == datetime(year=2017, month=1, day=1)
        assert df.end_date == datetime(year=2017, month=1, day=31)

    def test_quarter(self):
        df = self.skeleton()
        df.quarter = 1
        df.year = 2017
        df.save()

        assert df.start_date == datetime(year=2017, month=1, day=1)
        assert df.end_date == datetime(year=2017, month=3, day=31)
