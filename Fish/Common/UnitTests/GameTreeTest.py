import unittest
from Common.game_tree import GameTree
from Common.board import Board
from Common.state import GameState
from Common.Model.Player import Player

class TestGameTreeChildren(unittest.TestCase):

    def test_regular_behavior(self):
        """
        1   1   1           1   1   0           1   1   1
          1   1   0 --->      1   1   -1  OR      1   1   -1
        1   1   1           1   1   1           1   1   0

        Reminder: 0 is a penguin, -1 is a hole
        """

        board = Board(3, 3)
        board.make_uniform_board(1)
        player = Player(10, "red")

        state = GameState([player], board)
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        children = tree.get_children()

        self.assertEqual((player, (1, 2), (0, 2)), (player, (1, 2), (2, 2)))









    def test_no_moves_game_over(self):
        pass

    def test_no_moves_not_game_over(self):
        pass
