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
        moves = list(children.keys())
        moves.sort()

        self.assertEqual([(player, (1, 2), (0, 2)), (player, (1, 2), (2, 2))], moves)
        # -------
        first_move_board = Board(3, 3)
        first_move_board.make_uniform_board(1)
        first_move_board.add_hole((1, 2))
        first_move_player = Player(10, "red")
        first_move_state = GameState([first_move_player], board)
        first_move_state.place_penguin(first_move_player, (1, 0))
        first_move_resulting_tree = GameTree(first_move_state)
        self.assertEqual(first_move_resulting_tree, children[moves[0]])

        # --------
        second_move_board = Board(3, 3)
        second_move_board.make_uniform_board(1)
        second_move_board.add_hole((1, 2))
        second_move_player = Player(10, "red")
        second_move_state = GameState([second_move_player], board)
        second_move_state.place_penguin(second_move_player, (1, 0))
        second_move_resulting_tree = GameTree(second_move_state)
        second_move_resulting_tree = GameTree(second_move_resulting_tree)
        self.assertEqual(second_move_resulting_tree, children[moves[1]])


    def test_no_moves_game_over(self):
        pass

    def test_no_moves_not_game_over(self):
        pass


if __name__ == '__main__':
    unittest.main()