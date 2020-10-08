import unittest
import sys
sys.path.append('..')
from View.TileView import TileView

class TestTileViewYOffset(unittest.TestCase):

    def test_y_offset_odd_row_small(self):
        tile1 = TileView(3, 2, 'brown')
        self.assertEqual(TileView.TILE_SIZE * 3, tile1.get_y_offset())


    def test_y_offset_even_row(self):
        tile2 = TileView(6, 1, -1)
        self.assertEqual(TileView.TILE_SIZE * 6, tile2.get_y_offset())


    def test_y_offset_odd_row_big(self):
        tile3 = TileView(1, 1313, 1)
        self.assertEqual(TileView.TILE_SIZE * 1, tile3.get_y_offset())

class TestTileViewXOffset(unittest.TestCase):
    def test_x_offset_odd_row_small(self):
        tile1 = TileView(3, 2, 'brown')
        self.assertEqual(TileView.TILE_SIZE * 10, tile1.get_x_offset())


    def test_x_offset_even_row_small(self):
        tile2 = TileView(6, 1, -1)
        self.assertEqual(TileView.TILE_SIZE * 4, tile2.get_x_offset())


    def test_x_offset_odd_row_big(self):
        tile3 = TileView(1, 1313, 1)
        self.assertEqual(TileView.TILE_SIZE * 5254, tile3.get_x_offset())




class TestTileViewOutline(unittest.TestCase):

    def test_tile_outline(self):
        tile1 = TileView(2, 2, 4)
        outline = [TileView.TILE_SIZE*9, TileView.TILE_SIZE*2,
            TileView.TILE_SIZE*10, TileView.TILE_SIZE*2,
            TileView.TILE_SIZE*11, TileView.TILE_SIZE*3,
            TileView.TILE_SIZE*10, TileView.TILE_SIZE*4,
            TileView.TILE_SIZE*9, TileView.TILE_SIZE*4,
            TileView.TILE_SIZE*8, TileView.TILE_SIZE*3]
        self.assertEqual(outline, tile1.get_tile_outline())


if __name__ == '__main__':
    unittest.main()
