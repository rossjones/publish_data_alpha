from datetime import datetime, timedelta
import uuid

from django.test import TestCase

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)

from datasets.logic import (most_recent_datafile,
    number_days_for_frequency, is_dataset_overdue)

SOURCE_DATA = [
    {
        'name': 'one',
        'expected_overdue': False,
        'frequency': 'annually',
        'files': []
    },
    {
        'name': 'two',
        'frequency': 'annually',
        'expected_overdue': True,
        'files': [
            {
                'url': 'http://localhost/1.csv',
                'start_date': datetime(year=2015, month=1, day=1),
                'end_date': datetime(year=2015, month=12, day=31),
            },
            {
                'url': 'http://localhost/2.csv',
                'start_date': datetime(year=2014, month=1, day=1),
                'end_date': datetime(year=2014, month=12, day=31),
            },
            {
                'url': 'http://localhost/3.csv',
            }
        ]
    },
 {
        'name': 'three',
        'frequency': 'annually',
        'expected_overdue': False,
        'files': [
            {
                'url': 'http://localhost/1.csv',
                'start_date': datetime.now().date(),
                'end_date': datetime.now().date()
            }
        ]
    },
    {
        'name': 'four',
        'frequency': 'monthly',
        'expected_overdue': True,
        'files': [
            {
                'url': 'http://localhost/1.csv',
                'start_date': datetime(year=2016, month=1, day=1),
                'end_date': datetime(year=2016, month=12, day=31)
            }
        ]
    },
    {
        'name': 'five',
        'frequency': 'monthly',
        'expected_overdue': False,
        'files': [
            {
                'url': 'http://localhost/1.csv',
                'start_date': datetime.now().date(),
                'end_date': datetime.now().date()
            }
        ]
    },
]

class OverdueCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory.create()
        self.organisation = OrganisationFactory.create()
        self.organisation.users.add(self.test_user)
        self.datasets = []

        for d in SOURCE_DATA:
            dataset = DatasetFactory.create(
                name=d['name'],
                organisation_id=self.organisation.id,
                frequency=d['frequency']
            )

            for f in d['files']:
                args = {
                    'id': str(uuid.uuid4()),
                    'url': f['url'],
                    'dataset':dataset}
                if 'start_date' in f:
                    args['start_date'] = f['start_date']
                    args['end_date'] = f['end_date']

                DatafileFactory.create(**args)

            dataset.expected_overdue = d['expected_overdue']
            self.datasets.append(dataset)

    def test_most_recent(self):
        d = most_recent_datafile(self.datasets[1])
        assert d == datetime(year=2015,month=1,day=1).date()

    def test_overdue(self):
        # Get the most recent end-date from the dataset
        # make sure it was within 'frequency'
        assert len(self.datasets) == 5
        for dataset in self.datasets:
            overdue = is_dataset_overdue(dataset)
            if overdue and not dataset.expected_overdue:
                assert False, "Was overdue but not expected"
            if not overdue and dataset.expected_overdue:
                assert False, "Was not overdue and it should be"
