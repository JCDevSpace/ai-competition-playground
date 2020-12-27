from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from Game.Common.fish_board import FishBoard


class FishBoardTestUniformBoard(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

    def test_bad_num_fish(self):
        self.assertFalse(self.no_preset_board.make_uniform_board(0))
        self.assertFalse(self.no_preset_board.make_uniform_board(1000))

    def test_min_num_fish(self):
        self.assertTrue(self.no_preset_board.make_uniform_board(self.min_fish))

    def test_max_num_fish(self):
        self.assertTrue(self.no_preset_board.make_uniform_board(self.max_fish))
        
    def test_preset_layout(self):
        self.assertFalse(self.preset_board.make_uniform_board(self.min_fish))
        self.assertFalse(self.preset_board.make_limited_board(self.max_fish))


class FishBoardTestLimitedBoard(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])

    def test_bad_num_fish(self):
        self.assertFalse(self.no_preset_board.make_limited_board(0))
        self.assertFalse(self.no_preset_board.make_limited_board(self.rows * self.cols + 1))

    def test_small_num_fish(self):
        self.assertTrue(self.no_preset_board.make_limited_board(1))

    def test_meidum_num_fish(self):
        self.assertTrue(self.no_preset_board.make_limited_board(8))

    def test_large_num_fish(self):
        self.assertTrue(self.no_preset_board.make_limited_board(self.rows * self.cols))
    
    def test_preset_layout(self):
        self.assertFalse(self.preset_board.make_limited_board(10))
        self.assertFalse(self.preset_board.make_limited_board(5))


class FishBoardTestSetFish(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])


class FishBoardTestSetHole(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])


class FishBoardTestSetRandomHole(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])


class FishBoardTestFindValidActions(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])


class FishBoardTestApplyActions(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])


class FishBoardTestSerialize(unittest.TestCase):
    def setUp(self):
        self.min_fish = 1
        self.max_fish = 5
        self.rows = 4
        self.cols = 4
        self.no_preset_board = FishBoard(self.rows, self.cols, min_fish=self.min_fish, max_fish=self.max_fish)
        self.preset_board = FishBoard(0, 0, [[1,4,0,4], [2,2,3,0], [2,4,5,5]])


if __name__ == "__main__":
    unittest.main()