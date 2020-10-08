import sys
sys.path.append("..")

import unittest
from Model import Board

class BoardTestUniformBoard(unittest.TestCase):
	def test_uniform_board(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		self.assertEqual(b.get_board_state(), [[1, 1, 1], [1, 1, 1], [1, 1, 1]])

class BoardTestBoardMinOneFishTile(unittest.TestCase):
	def test_limited_board(self):
		b = Board.Board(3, 3)
		expected_one_fish_tile_count = 5
		b.make_limited_board(expected_one_fish_tile_count)

		board_state = b.get_board_state()
		one_fish_tile_count = 0
		for row in board_state:
			for tile in row:
				if tile == 1:
				  one_fish_tile_count += 1

		self.assertGreaterEqual(one_fish_tile_count, expected_one_fish_tile_count)

class BoardTestSetTile(unittest.TestCase):
	def test_set_tile_to_fish(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		b.set_tile(5, 1, 1)
		self.assertEqual(b.get_board_state(), [[1, 1, 1], [1, 5, 1], [1, 1, 1]])

	def test_set_tile_to_color(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		b.set_tile('red', 1, 1)
		self.assertEqual(b.get_board_state(), [[1, 1, 1], [1, 'red', 1], [1, 1, 1]])

	def test_set_tile_to_hole(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		b.set_tile(-1, 1, 1)
		self.assertEqual(b.get_board_state(), [[1, 1, 1], [1, -1, 1], [1, 1, 1]])


class BoardTestAddHole(unittest.TestCase):
	def test_add_hole(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		b.add_hole(1, 1)
		self.assertEqual(b.get_board_state(), [[1, 1, 1], [1, -1, 1], [1, 1, 1]])

class BoardTestHoleCount(unittest.TestCase):
	def test_hole_count(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		b.add_hole(0,0)
		b.add_hole(1,0)
		b.add_hole(1,2)
		self.assertEqual(b.hole_count(), 3)

class BoardTestGetValidMoves(unittest.TestCase):
	def test_get_valid_moves_from_even_row(self):
		b = Board.Board(5, 5)
		b.make_uniform_board(1)
		b.set_tile("red", 2, 2)
		self.assertEqual(b.get_valid_moves("red", 2, 2), [(4, 2), (0, 2), (1, 1), (0, 1), (1, 2), (0, 3), (3, 1), (4, 1), (3, 2), (4, 3)])

	def test_get_valid_moves_from_odd_row(self):
		b = Board.Board(5, 5)
		b.make_uniform_board(1)
		b.set_tile("red", 3, 3)
		self.assertEqual(b.get_valid_moves("red", 3, 3), [(1, 3), (2, 3), (1, 2), (0, 2), (2, 4), (1, 4), (4, 3), (4, 4)])

class BoardTestValidInDirection(unittest.TestCase):
	def test_valid_in_direction(self):
		b = Board.Board(5, 5)
		b.make_uniform_board(1)
		b.set_tile("red", 3, 3)
		self.assertEqual(b.valid_in_dir(3, 3, 2), [(2, 3), (1, 2), (0, 2)])

	def test_valid_in_direction_when_runs_into_hole(self):
		b = Board.Board(5, 5)
		b.make_uniform_board(1)
		b.set_tile("red", 3, 3)
		b.add_hole(1,2)
		self.assertEqual(b.valid_in_dir(3, 3, 2), [(2, 3)])

class BoardTestValidSquare(unittest.TestCase):
	def test_valid_tile(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		self.assertEqual(b.is_valid_square(1,1), True)

	def test_hole_tile(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		b.add_hole(1,1)
		self.assertEqual(b.is_valid_square(1,1), False)

	def test_out_of_bounds(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		self.assertEqual(b.is_valid_square(3,3), False)

	def test_penguin(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		b.set_tile("red", 1, 1)
		self.assertEqual(b.is_valid_square(1,1), False)

if __name__ == '__main__':
	unittest.main()
