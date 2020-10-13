import unittest
import sys
sys.path.append('..')
from View.TileArtist import TileArtist

class TestTileArtistYOffset(unittest.TestCase):

    def test_y_offset_odd_row_small(self):
        tile1 = TileArtist(3, 2, 'brown')
        self.assertEqual(TileArtist.TILE_SIZE * 3, tile1.get_y_offset())


    def test_y_offset_even_row(self):
        tile2 = TileArtist(6, 1, -1)
        self.assertEqual(TileArtist.TILE_SIZE * 6, tile2.get_y_offset())


    def test_y_offset_odd_row_big(self):
        tile3 = TileArtist(1, 1313, 1)
        self.assertEqual(TileArtist.TILE_SIZE * 1, tile3.get_y_offset())

class TestTileArtistXOffset(unittest.TestCase):
    def test_x_offset_odd_row_small(self):
        tile1 = TileArtist(3, 2, 'brown')
        self.assertEqual(TileArtist.TILE_SIZE * 10, tile1.get_x_offset())


    def test_x_offset_even_row_small(self):
        tile2 = TileArtist(6, 1, -1)
        self.assertEqual(TileArtist.TILE_SIZE * 4, tile2.get_x_offset())


    def test_x_offset_odd_row_big(self):
        tile3 = TileArtist(1, 1313, 1)
        self.assertEqual(TileArtist.TILE_SIZE * 5254, tile3.get_x_offset())




class TestTileArtistOutline(unittest.TestCase):

    def test_tile_outline(self):
        tile1 = TileArtist(2, 2, 4)
        outline = [TileArtist.TILE_SIZE*9, TileArtist.TILE_SIZE*2,
            TileArtist.TILE_SIZE*10, TileArtist.TILE_SIZE*2,
            TileArtist.TILE_SIZE*11, TileArtist.TILE_SIZE*3,
            TileArtist.TILE_SIZE*10, TileArtist.TILE_SIZE*4,
            TileArtist.TILE_SIZE*9, TileArtist.TILE_SIZE*4,
            TileArtist.TILE_SIZE*8, TileArtist.TILE_SIZE*3]
        self.assertEqual(outline, tile1.get_tile_outline())


if __name__ == '__main__':
    unittest.main()
