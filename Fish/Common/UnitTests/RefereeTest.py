import sys

sys.path.append('..')
import unittest
from Controller.Referee import Referee


class TestRefereeInitStandard(unittest.TestCase):

    def test_referee_init_nothing(self):
        r = Referee()
        # Seems like a nonsense test but is asserting that the constructor is valid
        self.assertEqual(True, True)

    def test_referee_init_rows_cols_big(self):
        r = Referee(rows=10, cols=100)
        # Seems like a nonsense test but is asserting that the constructor is valid
        self.assertEqual(True, True)

    def test_referee_init_rows_cols_regular(self):
        r = Referee(rows=5, cols=5)
        # Seems like a nonsense test but is asserting that the constructor is valid
        self.assertEqual(True, True)

    def test_referee_specific(self):
        r = Referee(rows=3, cols=3, specific_holes=[(0, 0), (2, 2)])
        self.assertEqual(True, True)

    def test_referee_min_holes(self):
        r = Referee(rows=3, cols=3, min_holes=8)
        self.assertEqual(True, True)

    def test_referee_min_one_fish(self):
        r = Referee(rows=3, cols=3, min_one_fish=8)
        self.assertEqual(True, True)

    def test_referee_min_holes_and_fish(self):
        r = Referee(rows=3, cols=3, min_holes=4, min_one_fish=4)
        self.assertEqual(True, True)

    def test_referee_min_holes_and_fish_and_specific(self):
        r = Referee(rows=3, cols=3, min_holes=4, min_one_fish=4,
                    specific_holes=[(0, 0), (0, 2), (2, 0)])
        self.assertEqual(True, True)


class TestRefereeInitError(unittest.TestCase):

    def test_referee_init_row_too_small(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=0)

    def test_referee_init_col_too_small(self):
        with self.assertRaises(ValueError):
            x = Referee(cols=0)

    def test_referee_init_missing_info(self):
        with self.assertRaises(ValueError):
            # missing uniform fish number
            x = Referee(uniform=True)

    def test_referee_init_too_many_conditions(self):
        with self.assertRaises(ValueError):
            x = Referee(uniform=True, min_holes=10)

    def test_referee_init_too_many_conditions_2(self):
        with self.assertRaises(ValueError):
            x = Referee(uniform=True, min_one_fish=10)

    def test_referee_init_too_many_specified(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=2, cols=2, min_holes=3, min_one_fish=2)

    def test_referee_init_too_many_specified_specific(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=2, cols=2, min_holes=1, min_one_fish=2, specific_holes=[(0, 0), (0, 1), (1, 0)])


if __name__ == '__main__':
    unittest.main()
