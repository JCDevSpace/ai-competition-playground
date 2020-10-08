import sys
sys.path.append('..')
import unittest

from View.TileView import TileView
from View.BoardView import BoardView

class TestBoardViewHeight(unittest.TestCase):

    def test_frame_height_3x3(self):
        threebythree = BoardView([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertEqual(4 * TileView.TILE_SIZE, threebythree.calculate_frame_height())

    def test_frame_height_4x2(self):
        fourbytwo = BoardView([[1, 1], [1, 1], [-1, 'red'], [3, 4]])
        self.assertEqual(5 * TileView.TILE_SIZE, fourbytwo.calculate_frame_height())

    def test_frame_height_2x5(self):
        twobyfive = BoardView([[1, -1, 'brown', 5, 2], [4, 2, 'white', -1, -1]])
        self.assertEqual(3 * TileView.TILE_SIZE, twobyfive.calculate_frame_height())


class TestBoardViewWidth(unittest.TestCase):
    def test_frame_width_3x3(self):
        threebythree = BoardView([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertEqual(13 * TileView.TILE_SIZE, threebythree.calculate_frame_width())

    def test_frame_width_4x2(self):
        fourbytwo = BoardView([[1, 1], [1, 1], [-1, 'red'], [3, 4]])
        self.assertEqual(9 * TileView.TILE_SIZE, fourbytwo.calculate_frame_width())

    def test_frame_width_2x5(self):
        twobyfive = BoardView([[1, -1, 'brown', 5, 2], [4, 2, 'white', -1, -1]])
        self.assertEqual(21 * TileView.TILE_SIZE, twobyfive.calculate_frame_width())


if __name__ == '__main__':
    unittest.main()
