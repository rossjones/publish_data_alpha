from django.test import TestCase

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)

from datasets.logic import dataset_list

class LogicCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory.create()
        self.organisation = OrganisationFactory.create()
        self.organisation.users.add(self.test_user)
        self.dataset1 = DatasetFactory.create(name='one',
            title='One',
            description='dataset one',
            summary='dataset one summary',
            owner=self.test_user,
            organisation_id=self.organisation.id)
        self.dataset2 = DatasetFactory.create(name='two',
            title='Two',
            description='dataset two',
            summary='dataset two summary',
            owner=self.test_user,
            organisation_id=self.organisation.id)
        self.dataset3 = DatasetFactory.create(name='three',
            title='Three',
            description='dataset three',
            summary='dataset three summary',
            organisation_id=self.organisation.id)

    def test_list(self):
        total, _, l = dataset_list(self.test_user)
        assert total == 3, total

    def test_list_filter(self):
        total, _, l = dataset_list(self.test_user, filter_query='two')
        assert total == 1, total

    def test_list_useronly(self):
        total, _, l = dataset_list(self.test_user, only_user=True)
        assert total == 2, total

    def test_list_limited(self):
        # dataset_list(user, page=1, filter_query=None, sort=None, only_user = False):
        total, _, l = dataset_list(self.test_user, fields=['name', 'title'])
        d1, _, _ = l
        assert len(d1.keys()) == 2
        assert 'name' in d1
        assert 'title' in d1

    def test_list_limited_filter(self):
        total, _, l = dataset_list(
            self.test_user,
            filter_query='one',
            fields=['name', 'title']
        )

        assert len(l) == 1
        assert len(l[0].keys()) == 2
        assert 'name' in l[0]
        assert 'title' in l[0]
