import unittest

from Common.View.FishView import FishView
from Common.View.FishView import DEFAULT_STYLE

threebythree = FishView(([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [], {}, 0, {}))
fourbytwo = FishView(([[1, 1], [1, 1], [-1, 0], [3, 4]], [], {}, 0, {}))
twobyfive = FishView(([[1, -1, 0, 5, 2], [4, 2, 0, -1, -1]], [], {}, 0, {}))

class TestFishViewHeight(unittest.TestCase):
    def test_frame_height_3x3(self):
        self.assertEqual(4 * DEFAULT_STYLE['tile_size'], threebythree.calculate_frame_height())

    def test_frame_height_4x2(self):
        self.assertEqual(5 * DEFAULT_STYLE['tile_size'], fourbytwo.calculate_frame_height())

    def test_frame_height_2x5(self):
        self.assertEqual(3 * DEFAULT_STYLE['tile_size'], twobyfive.calculate_frame_height())

class TestFishViewWidth(unittest.TestCase):
    def test_frame_width_3x3(self):
        self.assertEqual(17 * DEFAULT_STYLE['tile_size'], threebythree.calculate_frame_width())

    def test_frame_width_4x2(self):
        self.assertEqual(13 * DEFAULT_STYLE['tile_size'], fourbytwo.calculate_frame_width())

    def test_frame_width_2x5(self):
        self.assertEqual(25 * DEFAULT_STYLE['tile_size'], twobyfive.calculate_frame_width())

if __name__ == '__main__':
    unittest.main()
