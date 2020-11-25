import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

import unittest

from Common.View.tile_artist import TileArtist
from Common.View.fish_view import DEFAULT_STYLE

class TestTileArtistOutline(unittest.TestCase):
    def test_tile_outline(self):
        tile1 = TileArtist(DEFAULT_STYLE['tile_size'] * 8,
                           DEFAULT_STYLE['tile_size'] * 2,
                           4,
                           [],
                           DEFAULT_STYLE)

        outline = [DEFAULT_STYLE['tile_size'] * 9, DEFAULT_STYLE['tile_size'] * 2,
                   DEFAULT_STYLE['tile_size'] * 10, DEFAULT_STYLE['tile_size'] * 2,
                   DEFAULT_STYLE['tile_size'] * 11, DEFAULT_STYLE['tile_size'] * 3,
                   DEFAULT_STYLE['tile_size'] * 10, DEFAULT_STYLE['tile_size'] * 4,
                   DEFAULT_STYLE['tile_size'] * 9, DEFAULT_STYLE['tile_size'] * 4,
                   DEFAULT_STYLE['tile_size'] * 8, DEFAULT_STYLE['tile_size'] * 3]

        self.assertEqual(outline, tile1.get_tile_outline())


if __name__ == '__main__':
    unittest.main()
