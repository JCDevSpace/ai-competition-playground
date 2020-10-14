import unittest
import sys
sys.path.append('..')
from View.TileArtist import TileArtist
from View.FishView import DEFAULT_STYLE

# class TestTileArtistYOffset(unittest.TestCase):
#
#     def test_y_offset_odd_row_small(self):
#         tile1 = TileArtist(3, 2, 0, DEFAULT_STYLE)
#         self.assertEqual(DEFAULT_STYLE['tile_size'] * 3, tile1.get_y_offset())
#
#
#     def test_y_offset_even_row(self):
#         tile2 = TileArtist(6, 1, -1, DEFAULT_STYLE)
#         self.assertEqual(DEFAULT_STYLE['tile_size']* 6, tile2.get_y_offset())
#
#
#     def test_y_offset_odd_row_big(self):
#         tile3 = TileArtist(1, 1313, 1, DEFAULT_STYLE)
#         self.assertEqual(DEFAULT_STYLE['tile_size'] * 1, tile3.get_y_offset())
#
# class TestTileArtistXOffset(unittest.TestCase):
#     def test_x_offset_odd_row_small(self, DEFAULT_STYLE):
#         tile1 = TileArtist(3, 2, 0, DEFAULT_STYLE)
#         self.assertEqual(DEFAULT_STYLE['tile_size'] * 10, tile1.get_x_offset())
#
#
#     def test_x_offset_even_row_small(self):
#         tile2 = TileArtist(6, 1, -1, DEFAULT_STYLE)
#         self.assertEqual(DEFAULT_STYLE['tile_size']* 4, tile2.get_x_offset())
#
#
#     def test_x_offset_odd_row_big(self):
#         tile3 = TileArtist(1, 1313, 1, DEFAULT_STYLE)
#         self.assertEqual(DEFAULT_STYLE['tile_size'] * 5254, tile3.get_x_offset())
#



class TestTileArtistOutline(unittest.TestCase):

    def test_tile_outline(self):
        tile1 = TileArtist(DEFAULT_STYLE['tile_size'] * 8,
                            DEFAULT_STYLE['tile_size'] * 2,
                            4,
                            DEFAULT_STYLE)

        outline = [DEFAULT_STYLE['tile_size']*9, DEFAULT_STYLE['tile_size']*2,
            DEFAULT_STYLE['tile_size']*10, DEFAULT_STYLE['tile_size']*2,
            DEFAULT_STYLE['tile_size']*11, DEFAULT_STYLE['tile_size']*3,
            DEFAULT_STYLE['tile_size']*10, DEFAULT_STYLE['tile_size']*4,
            DEFAULT_STYLE['tile_size']*9, DEFAULT_STYLE['tile_size']*4,
            DEFAULT_STYLE['tile_size']*8, DEFAULT_STYLE['tile_size']*3]

        self.assertEqual(outline, tile1.get_tile_outline())


if __name__ == '__main__':
    unittest.main()
