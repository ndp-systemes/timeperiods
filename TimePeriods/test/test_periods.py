import unittest
from datetime import datetime

from .. import TimePeriod, TimePeriodSet, INFINITY_BEGIN, INFINITY_END


class PeriodSetTest(unittest.TestCase):
    def setUp(self):
        super(PeriodSetTest, self).setUp()

        self.period_set = TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
        )
        self.other_period_set = TimePeriodSet(
            TimePeriod(datetime(1994, 1, 29), datetime(1994, 2, 7)),
            TimePeriod(datetime(1994, 2, 24), datetime(1994, 3, 5)),
            TimePeriod(datetime(1994, 3, 27), datetime(1994, 3, 29)),
            TimePeriod(datetime(1994, 7, 1), datetime(1994, 7, 28)),
            TimePeriod(datetime(1994, 10, 28), datetime(1994, 12, 8)),
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
        self.period_set |= TimePeriod(
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
        self.period_set |= TimePeriod(
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
        self.period_set |= TimePeriod(
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
        self.period_set |= TimePeriod(
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
        self.period_set |= TimePeriod(
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
        self.period_set |= TimePeriod(
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

    def test_30_union_between_sets(self):
        self.assertEqual(self.period_set | self.other_period_set, TimePeriodSet(
            TimePeriod(datetime(1994, 1, 29), datetime(1994, 3, 5)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 7, 1), datetime(1994, 7, 28)),
            TimePeriod(datetime(1994, 10, 28), datetime(1994, 12, 8)),
        ))

    def test_31_ensure_binary_union_works_like_unary(self):
        new = self.period_set | self.other_period_set
        self.assertNotEqual(self.period_set, new)
        self.period_set |= self.other_period_set
        self.assertEqual(self.period_set, new)

    def test_40_intersection_between_sets(self):
        self.assertEqual(self.period_set & self.other_period_set, TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 7)),
            TimePeriod(datetime(1994, 2, 24), datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 27), datetime(1994, 3, 29)),
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
        ))

    def test_41_ensure_binary_intersection_works_like_unary(self):
        new = self.period_set & self.other_period_set
        self.assertNotEqual(self.period_set, new)
        self.period_set &= self.other_period_set
        self.assertEqual(self.period_set, new)

    def test_50_infinite_begin_period_ending_before(self):
        infinite_begin_period = TimePeriodSet(TimePeriod(INFINITY_BEGIN, datetime(1994, 1, 1)))
        expected_union = TimePeriodSet(
            TimePeriod(INFINITY_BEGIN, datetime(1994, 1, 1)),
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
        )
        self.assertEqual(infinite_begin_period | self.period_set, expected_union)
        self.assertEqual(self.period_set | infinite_begin_period, expected_union)
        self.assertEqual(infinite_begin_period & self.period_set, TimePeriodSet())
        self.assertEqual(self.period_set & infinite_begin_period, TimePeriodSet())

    def test_51_infinite_begin_period_ending_in_period(self):
        infinite_begin_period = TimePeriodSet(TimePeriod(INFINITY_BEGIN, datetime(1994, 2, 7)))
        expected_union = TimePeriodSet(
            TimePeriod(INFINITY_BEGIN, datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
        )
        expected_intersection = TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 7))
        )
        self.assertEqual(infinite_begin_period | self.period_set, expected_union)
        self.assertEqual(self.period_set | infinite_begin_period, expected_union)
        self.assertEqual(infinite_begin_period & self.period_set, expected_intersection)
        self.assertEqual(self.period_set & infinite_begin_period, expected_intersection)

    def test_52_infinite_begin_period_ending_after_period(self):
        infinite_begin_period = TimePeriodSet(TimePeriod(INFINITY_BEGIN, datetime(1994, 3, 7)))
        expected_union = TimePeriodSet(
            TimePeriod(INFINITY_BEGIN, datetime(1994, 3, 7)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
        )
        expected_intersection = TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28))
        )
        self.assertEqual(infinite_begin_period | self.period_set, expected_union)
        self.assertEqual(self.period_set | infinite_begin_period, expected_union)
        self.assertEqual(infinite_begin_period & self.period_set, expected_intersection)
        self.assertEqual(self.period_set & infinite_begin_period, expected_intersection)

    def test_60_infinite_end_period_beginning_after(self):
        infinite_end_period = TimePeriodSet(TimePeriod(datetime(1994, 12, 8), INFINITY_END))
        expected_union = TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30)),
            TimePeriod(datetime(1994, 12, 8), INFINITY_END),
        )
        self.assertEqual(infinite_end_period | self.period_set, expected_union)
        self.assertEqual(self.period_set | infinite_end_period, expected_union)
        self.assertEqual(infinite_end_period & self.period_set, TimePeriodSet())
        self.assertEqual(self.period_set & infinite_end_period, TimePeriodSet())

    def test_61_infinite_end_period_beginning_in_period(self):
        infinite_end_period = TimePeriodSet(TimePeriod(datetime(1994, 11, 27), INFINITY_END))
        expected_union = TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 11, 1), INFINITY_END),
        )
        expected_intersection = TimePeriodSet(
            TimePeriod(datetime(1994, 11, 27), datetime(1994, 11, 30))
        )
        self.assertEqual(infinite_end_period | self.period_set, expected_union)
        self.assertEqual(self.period_set | infinite_end_period, expected_union)
        self.assertEqual(infinite_end_period & self.period_set, expected_intersection)
        self.assertEqual(self.period_set & infinite_end_period, expected_intersection)

    def test_62_infinite_end_period_ending_before_period(self):
        infinite_end_period = TimePeriodSet(TimePeriod(datetime(1994, 10, 30), INFINITY_END))
        expected_union = TimePeriodSet(
            TimePeriod(datetime(1994, 2, 1), datetime(1994, 2, 28)),
            TimePeriod(datetime(1994, 3, 22), datetime(1994, 4, 1)),
            TimePeriod(datetime(1994, 10, 30), INFINITY_END),
        )
        expected_intersection = TimePeriodSet(
            TimePeriod(datetime(1994, 11, 1), datetime(1994, 11, 30))
        )
        self.assertEqual(infinite_end_period | self.period_set, expected_union)
        self.assertEqual(self.period_set | infinite_end_period, expected_union)
        self.assertEqual(infinite_end_period & self.period_set, expected_intersection)
        self.assertEqual(self.period_set & infinite_end_period, expected_intersection)

    def test_70_infinite_begin_and_end_period(self):
        infinite_period = TimePeriodSet(TimePeriod(INFINITY_BEGIN, INFINITY_END))
        expected_union = infinite_period
        expected_intersection = self.period_set
        self.assertEqual(infinite_period | self.period_set, expected_union)
        self.assertEqual(self.period_set | infinite_period, expected_union)
        self.assertEqual(infinite_period & self.period_set, expected_intersection)
        self.assertEqual(self.period_set & infinite_period, expected_intersection)


if __name__ == '__main__':
    unittest.main()
