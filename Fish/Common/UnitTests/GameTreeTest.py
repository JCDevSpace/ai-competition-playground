import unittest
from Common.game_tree import GameTree
from Common.board import Board
from Common.state import GameState
from Common.Model.Player import Player


class TestGameTreeGetGameState(unittest.TestCase):
    pass


class TestGameTreeResultingState(unittest.TestCase):
    pass


class TestGameTreeGetChildren(unittest.TestCase):

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

        # ------- check child 1
        first_move_board = [[1, 1, 0], [1, 1, -1], [1, 1, 1]]
        first_move_players = [player.get_data()]
        first_move_penguin_positions = {'red': {(0, 2)}}
        first_move_turn = 0
        first_move_score = {'red': 2}
        first_move_state = (first_move_board, first_move_players,
                            first_move_penguin_positions, first_move_turn, first_move_score)
        self.assertEqual(first_move_state, children[moves[0]].get_current_state().get_game_state())

        # -------- check child 2
        second_move_board = [[1, 1, 1], [1, 1, -1], [1, 1, 0]]
        second_move_players = [player.get_data()]
        second_move_penguin_positions = {'red': {(2, 2)}}
        second_move_turn = 0
        second_move_score = {'red': 2}
        second_move_state = (second_move_board, second_move_players,
                             second_move_penguin_positions, second_move_turn, second_move_score)
        self.assertEqual(second_move_state, children[moves[1]].get_current_state().get_game_state())

    def test_no_moves_game_over(self):
        """
                1   1   -1
                  1   1   0 --->   No moves, game over
                1   1   -1

                Reminder: 0 is a penguin, -1 is a hole
                """

        board = Board(3, 3)
        board.make_uniform_board(1)
        board.add_hole((0, 2))
        board.add_hole((2, 2))
        player = Player(10, "red")
        state = GameState([player], board)
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        children = tree.get_children()

        self.assertEqual({}, children)



    def test_no_moves_not_game_over(self):
        """
        1   1   -1  (turn 0 )                   1   1   -1
          0   1   0 --->   No moves, for me, ->   0   1    0 (turn 1)
        1   1   -1          yes for others      1   1   -1

        Reminder: 0 is a penguin, -1 is a hole
        """

        board = Board(3, 3)
        board.make_uniform_board(1)
        board.add_hole((0, 2))
        board.add_hole((2, 2))
        player = Player(10, "red")
        player2 = Player(1000, "black")
        state = GameState([player, player2], board)
        state.place_penguin(player, (1, 2))
        state.place_penguin(player2, (1, 0))
        tree = GameTree(state)
        children = tree.get_children()
        moves = list(children.keys())
        moves.sort()

        self.assertEqual((player, False), moves)

        first_move_board = [[1, 1, -1], [0, 1, 0], [1, 1, -1]]
        first_move_players = [player.get_data(), player2.get_data()]
        first_move_penguin_positions = {'red': {(1, 2)}, 'black': {(1, 0)}}
        first_move_turn = 1
        first_move_score = {'red': 1, 'black' : 1}
        first_move_state = (first_move_board, first_move_players,
                            first_move_penguin_positions, first_move_turn, first_move_score)
        self.assertEqual(first_move_state, children[moves[0]].get_current_state().get_game_state())


class TestGameTreeApply(unittest.TestCase):
    pass



if __name__ == '__main__':
    unittest.main()