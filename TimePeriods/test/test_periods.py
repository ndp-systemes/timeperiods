import unittest
from datetime import datetime

from .. import TimePeriod, TimePeriodSet


class PeriodSetTest(unittest.TestCase):
    def setUp(self):
        super(PeriodSetTest, self).setUp()

        self.period_set = TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
        )

    def test_00_period_equals(self):
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_01_unequal_if_period_begin_differs(self):
        self.assertNotEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 23), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_02_unequal_if_period_end_differs(self):
        self.assertNotEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 2)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_03_unequal_if_period_missing(self):
        self.assertNotEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_04_unequal_if_more_period(self):
        self.assertNotEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 6, 1), datetime(1994, 6, 30)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_05_unequal_if_one_period_differ(self):
        self.assertNotEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 6, 1), datetime(1994, 6, 30)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_10_union_period_overlapping_end(self):
        self.period_set += TimePeriod(
            datetime(1994, 2, 27),
            datetime(1994, 3, 10)
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 3, 10)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_11_union_period_overlapping_start(self):
        self.period_set += TimePeriod(
            datetime(1994, 3, 10),
            datetime(1994, 3, 23)
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 10), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_12_union_period_overlapping_both(self):
        self.period_set += TimePeriod(
            datetime(1994, 2, 27),
            datetime(1994, 3, 23)
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_13_union_period_not_overlapping(self):
        self.period_set += TimePeriod(
            datetime(1994, 6, 1),
            datetime(1994, 6, 30),
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 6, 1), datetime(1994, 6, 30)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_14_union_period_including(self):
        self.period_set += TimePeriod(
            datetime(1994, 1, 20),
            datetime(1994, 3, 10),
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 1, 20), datetime(1994, 3, 10)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_15_union_period_included(self):
        self.period_set += TimePeriod(
            datetime(1994, 2, 7),
            datetime(1994, 2, 14),
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
                TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            ),
        )

    def test_20_intersect_period_overlapping_end(self):
        self.period_set &= TimePeriod(
            datetime(1994, 2, 27),
            datetime(1994, 3, 10)
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 27), datetime(1994, 2, 28)),
            ),
        )

    def test_21_intersect_period_overlapping_start(self):
        self.period_set &= TimePeriod(
            datetime(1994, 3, 10),
            datetime(1994, 3, 23)
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 3, 23)),
            ),
        )

    def test_22_intersect_period_overlapping_both(self):
        self.period_set &= TimePeriod(
            datetime(1994, 2, 27),
            datetime(1994, 3, 23)
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 27), datetime(1994, 2, 28)),
                TimePeriod(datetime(1994, 3, 22), datetime(1994, 3, 23)),
            ),
        )

    def test_23_intersect_period_not_overlapping(self):
        self.period_set &= TimePeriod(
            datetime(1994, 6, 1),
            datetime(1994, 6, 30),
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(),
        )

    def test_24_intersect_period_including(self):
        self.period_set &= TimePeriod(
            datetime(1994, 1, 20),
            datetime(1994, 3, 10),
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
            ),
        )

    def test_25_intersect_period_included(self):
        self.period_set &= TimePeriod(
            datetime(1994, 2, 7),
            datetime(1994, 2, 14),
        )
        self.assertEqual(
            self.period_set,
            TimePeriodSet(
                TimePeriod(datetime(1994, 2, 7), datetime(1994, 2, 14)),
            ),
        )


if __name__ == '__main__':
    unittest.main()
