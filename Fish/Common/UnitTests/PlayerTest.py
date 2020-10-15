import sys

sys.path.append("..")
import unittest
from Model.Player import Player


class TestPlayerColor(unittest.TestCase):

    def test_get_color(self):
        p = Player(10, 'brown')
        self.assertEqual('brown', p.get_color())


class TestPlayerAge(unittest.TestCase):
    def test_get_age(self):
        p = Player(12, 'brown')
        self.assertEqual(12, p.get_age())


# class TestPlayerLT(unittest.TestCase):
#     def test_lt_true(self):
#         p1 = Player(12, 'brown')
#         p2 = Player(13, 'white')
#         self.assertEqual(True, p1 < p2)
#
#     def test_lt_false(self):
#         p2 = Player(13, 'white')
#         p3 = Player(14, 'red')
#         self.assertEqual(False, p3 < p2)
#
#
#
# class TestPlayerGT(unittest.TestCase):
#     def test_gt_true(self):
#         p1 = Player(15, 'red')
#         p2 = Player(1, 'black')
#         self.assertEqual(True, p1 > p2)
#
#     def test_gt_false(self):
#         p1 = Player(15, 'red')
#         p3 = Player(30, 'white')
#         self.assertEqual(False, p1 > p3)


class TestPlayerEQ(unittest.TestCase):
    def test_eq_true(self):
        p1 = Player(96, 'red')
        p2 = Player(99, 'red')
        self.assertEqual(True, p1 == p2)

    def test_eq_false(self):
        p1 = Player(99, 'red')
        p3 = Player(99, 'white')
        self.assertEqual(False, p1 == p3)


if __name__ == '__main__':
    unittest.main()
