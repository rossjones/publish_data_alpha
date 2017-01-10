from django.test import TestCase

from datasets.util import (calculate_dates_for_year,
                         calculate_dates_for_month,
                         calculate_dates_for_quarter)


class DatesTestCase(TestCase):

    def test_years(self):
        (sd, ed) = calculate_dates_for_year(2017)

        assert sd.year == 2017
        assert sd.month == 1
        assert sd.day == 1

        assert ed.year == 2017
        assert ed.month == 12
        assert ed.day == 31

    def test_month(self):
        (sd, ed) = calculate_dates_for_month(2, 2009)

        assert sd.year == 2009
        assert sd.month == 2
        assert sd.day == 1

        assert ed.year == 2009
        assert ed.month == 2
        assert ed.day == 28

    def test_month_leapyear(self):
        (sd, ed) = calculate_dates_for_month(2, 2012)

        assert sd.year == 2012
        assert sd.month == 2
        assert sd.day == 1

        assert ed.year == 2012
        assert ed.month == 2
        assert ed.day == 29

    def test_q1(self):
        (sd, ed) = calculate_dates_for_quarter(1, 2010)

        assert sd.month == 1
        assert sd.day == 1

        assert ed.month == 3
        assert ed.day == 31

        assert ed.year == sd.year == 2010

    def test_q2(self):
        (sd, ed) = calculate_dates_for_quarter(2, 2010)

        assert sd.month == 4
        assert sd.day == 1

        assert ed.month == 6
        assert ed.day == 30

        assert ed.year == sd.year == 2010

    def test_q3(self):
        (sd, ed) = calculate_dates_for_quarter(3, 2010)

        assert sd.month == 7
        assert sd.day == 1

        assert ed.month == 9
        assert ed.day == 30

        assert ed.year == sd.year == 2010

    def test_q4(self):
        (sd, ed) = calculate_dates_for_quarter(4, 2010)

        assert sd.month == 10
        assert sd.day == 1

        assert ed.month == 12
        assert ed.day == 31

        assert ed.year == sd.year == 2010
