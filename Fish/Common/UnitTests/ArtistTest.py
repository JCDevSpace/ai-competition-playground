import unittest

from Common.View.Artist import Artist
from Common.View.FishView import DEFAULT_STYLE

class TestArtistXOffset(unittest.TestCase):
    def test_x_offset_odd_row_small(self):
        tile1 = Artist(DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 10, tile1.calculate_x_offset(1, 2))


    def test_x_offset_even_row_small(self):
        tile2 = Artist( DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size']* 4, tile2.calculate_x_offset(0, 1))


    def test_x_offset_odd_row_big(self):
        tile3 = Artist(DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 5254, tile3.calculate_x_offset(1, 1313))


class TestArtistYOffset(unittest.TestCase):
    def test_y_offset_odd_row_small(self):
        tile1 = Artist(DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 3, tile1.calculate_y_offset(3))


    def test_y_offset_even_row(self):
        tile2 = Artist( DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size']* 6, tile2.calculate_y_offset(6))


    def test_y_offset_odd_row_big(self):
        tile3 = Artist(DEFAULT_STYLE)
        self.assertEqual(DEFAULT_STYLE['tile_size'] * 1, tile3.calculate_y_offset(1))

class TestArtistTileCenter(unittest.TestCase):
    def test_row_center(self):
        tile1 = Artist(DEFAULT_STYLE)
        self.assertEqual((int(DEFAULT_STYLE['tile_size'] * 11.5), DEFAULT_STYLE['tile_size'] * 4),
            tile1.get_tile_center(DEFAULT_STYLE['tile_size'] * 10, DEFAULT_STYLE['tile_size'] * 3))

if __name__ == '__main__':
    unittest.main()
