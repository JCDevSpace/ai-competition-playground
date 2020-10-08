import sys
sys.path.append("..")

import unittest
from Model import Board

class BoardTestUniformBoard(unittest.TestCase):
	def test_uniform_board(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		self.assertEqual(b.get_board_state(), [[1, 1, 1], [1, 1, 1], [1, 1, 1]])

class BoardTestUniformBoard(unittest.TestCase):
	def test_uniform_board(self):
		b = Board.Board(3, 3)
		b.make_uniform_board(1)
		self.assertEqual(b.get_board_state(), [[1, 1, 1], [1, 1, 1], [1, 1, 1]])

if __name__ == '__main__':
	unittest.main()
