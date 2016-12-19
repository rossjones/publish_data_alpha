from datetime import datetime

from django.test import TestCase

from stats.models import OrganisationStatistic
from stats.logic import get_stats


class StatsTestCase(TestCase):

    def setUp(self):
        self.stat = OrganisationStatistic.objects.create(
            organisation_name="cabinet-office",
            subject_title="Downloads",
            dataset_title="Made up title",
            value=125,
            direction="up",
            since="+1% since yesterday",
            timestamp=datetime.now()
        )

    def test_get_stats(self):
        stats = get_stats("cabinet-office", "Downloads")
        assert len(stats) == 1

    def test_get_no_stats(self):
        stats = get_stats("cabinet-office", "Views")
        assert len(stats) == 0
