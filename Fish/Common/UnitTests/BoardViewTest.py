import sys
sys.path.append('..')
import unittest

from View.FishView import DEFAULT_STYLE
from View.BoardArtist import BoardArtist


# class TestBoardArtistHeight(unittest.TestCase):
#
#     def test_frame_height_3x3(self):
#         game_state
#         threebythree = BoardArtist([[1, 1, 1], [1, 1, 1], [1, 1, 1]], DEFAULT_STYLE)
#         self.assertEqual(4 * DEFAULT_STYLE['tile_size'], threebythree.calculate_frame_height())
#
#     def test_frame_height_4x2(self):
#         fourbytwo = BoardArtist([[1, 1], [1, 1], [-1, 0], [3, 4]], DEFAULT_STYLE)
#         self.assertEqual(5 * DEFAULT_STYLE['tile_size'], fourbytwo.calculate_frame_height())
#
#     def test_frame_height_2x5(self):
#         twobyfive = BoardArtist([[1, -1, 0, 5, 2], [4, 2, 0, -1, -1]], DEFAULT_STYLE)
#         self.assertEqual(3 * DEFAULT_STYLE['tile_size'], twobyfive.calculate_frame_height())
#
#
# class TestBoardArtistWidth(unittest.TestCase):
#     def test_frame_width_3x3(self):
#         threebythree = BoardArtist([[1, 1, 1], [1, 1, 1], [1, 1, 1]], DEFAULT_STYLE)
#         self.assertEqual(13 * DEFAULT_STYLE['tile_size'], threebythree.calculate_frame_width())
#
#     def test_frame_width_4x2(self):
#         fourbytwo = BoardArtist([[1, 1], [1, 1], [-1, 0], [3, 4]],DEFAULT_STYLE)
#         self.assertEqual(9 * DEFAULT_STYLE['tile_size'], fourbytwo.calculate_frame_width())
#
#     def test_frame_width_2x5(self):
#         twobyfive = BoardArtist([[1, -1, 0, 5, 2], [4, 2, 0, -1, -1]], DEFAULT_STYLE)
#         self.assertEqual(21 * DEFAULT_STYLE['tile_size'], twobyfive.calculate_frame_width())

class TestBoardArtistYOffset(unittest.TestCase):

    def test_y_offset_odd_row_small(self):
        board1 = BoardArtist([[]], DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 3, board1.calculate_y_offset(3))

    def test_y_offset_even_row(self):
        board2 = BoardArtist([[]], DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 6, board2.calculate_y_offset(6))

    def test_y_offset_odd_row_big(self):
        board3 = BoardArtist([[]], DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 1, board3.calculate_y_offset(1))


class TestBoardArtistXOffset(unittest.TestCase):
    def test_x_offset_odd_row_small(self):
        board1 = BoardArtist([[]], DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 10, board1.calculate_x_offset(3, 2))

    def test_x_offset_even_row_small(self):
        board2 = BoardArtist([[]], DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 4, board2.calculate_x_offset(6, 1))

    def test_x_offset_odd_row_big(self):
        board3 = BoardArtist([[]], DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 5254, board3.calculate_x_offset(1, 1313))


if __name__ == '__main__':
    unittest.main()
