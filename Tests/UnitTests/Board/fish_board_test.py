from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../.."))

import unittest
from Game.Common.fish_board import FishBoard

class FishBoardTestUniformBoard(unittest.TestCase):
    
    def test_bad_num_fish(self):
        board = FishBoard(2, 2, )