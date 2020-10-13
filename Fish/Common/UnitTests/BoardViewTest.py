import sys
sys.path.append('..')
import unittest

from View.TileArtist import TileArtist
from View.BoardArtist import BoardArtist

class TestBoardArtistHeight(unittest.TestCase):

    def test_frame_height_3x3(self):
        threebythree = BoardArtist([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertEqual(4 * TileArtist.TILE_SIZE, threebythree.calculate_frame_height())

    def test_frame_height_4x2(self):
        fourbytwo = BoardArtist([[1, 1], [1, 1], [-1, 'red'], [3, 4]])
        self.assertEqual(5 * TileArtist.TILE_SIZE, fourbytwo.calculate_frame_height())

    def test_frame_height_2x5(self):
        twobyfive = BoardArtist([[1, -1, 'brown', 5, 2], [4, 2, 'white', -1, -1]])
        self.assertEqual(3 * TileArtist.TILE_SIZE, twobyfive.calculate_frame_height())


class TestBoardArtistWidth(unittest.TestCase):
    def test_frame_width_3x3(self):
        threebythree = BoardArtist([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.assertEqual(13 * TileArtist.TILE_SIZE, threebythree.calculate_frame_width())

    def test_frame_width_4x2(self):
        fourbytwo = BoardArtist([[1, 1], [1, 1], [-1, 'red'], [3, 4]])
        self.assertEqual(9 * TileArtist.TILE_SIZE, fourbytwo.calculate_frame_width())

    def test_frame_width_2x5(self):
        twobyfive = BoardArtist([[1, -1, 'brown', 5, 2], [4, 2, 'white', -1, -1]])
        self.assertEqual(21 * TileArtist.TILE_SIZE, twobyfive.calculate_frame_width())


if __name__ == '__main__':
    unittest.main()
