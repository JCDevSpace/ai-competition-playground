import unittest
from Common.game_tree import GameTree
from Common.board import Board
from Common.state import GameState

class TestGameTreeGetCurrentGameState(unittest.TestCase):

    def test_regular_current_state(self):
        board = Board(3, 3)
        board.make_uniform_board(1)
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)

        state2 = tree.get_current_state()

        self.assertEqual(state2.get_game_state(), state.get_game_state())

    def test_not_mutated_penguins_current_state(self):
        board = Board(3, 3)
        board.make_uniform_board(1)
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)

        state2 = tree.get_current_state()

        state.place_penguin(player, (0, 0))

        self.assertNotEqual(state2.get_game_state(), state.get_game_state())


class TestGameTreeResultingState(unittest.TestCase):

    def test_regular_resulting_state(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        tree2 = tree.resulting_state((player, (1, 2), (0, 2)))
        tree2_gamestate = tree2.get_current_state()

        resulting_board = [[1, 1, 1], [1, 1, 0], [1, 1, 1]]
        resulting_players = [player]
        resulting_penguin_positions = {'red': [(0, 2)]}
        resulting_turn = 0
        resulting_score = {'red': 1}
        resulting_state = (resulting_board, resulting_players,
                           resulting_penguin_positions, resulting_turn, resulting_score)

        self.assertEqual(tree2_gamestate.get_game_state(), resulting_state)

    def test_resulting_skipped_turn(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        board.add_hole((0, 2))
        board.add_hole((2, 2))
        player = "red"
        player2 = "brown"
        state = GameState(board, [player, player2], penguin_positions={}, turn=0, scores={})
        state.place_penguin(player, (1, 2))
        state.place_penguin(player2, (2, 0))
        state = state.deepcopy()
        tree = GameTree(state)
        tree_state = tree.get_current_state()

        beginning_board = [[1, 1, 0], [1, 1, 1], [1, 1, 0]]
        beginning_players = [player, player2]
        beginning_penguin_positions = {'red': [(1, 2)], 'brown': [(2, 0)]}
        beginning_turn = 0
        beginning_score = {'red': 0, 'brown': 0}
        beginning_state = (beginning_board, beginning_players,
                           beginning_penguin_positions, beginning_turn, beginning_score)
        self.assertEqual(beginning_state, tree_state.get_game_state())


        tree2 = tree.resulting_state((player, False))
        tree2_state = tree2.get_current_state().deepcopy()

        resulting_board = [[1, 1, 0], [1, 1, 1], [1, 1, 0]]
        resulting_players = [player, player2]
        resulting_penguin_positions = {'red': [(1, 2)], 'brown': [(2, 0)]}
        resulting_turn = 1
        resulting_score = {'red': 0, 'brown': 0}
        resulting_state = (resulting_board, resulting_players,
                           resulting_penguin_positions, resulting_turn, resulting_score)

        self.assertEqual(resulting_state, tree2_state.get_game_state())

    def test_resulting_invalid_posn(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        tree2 = tree.resulting_state((player, (1, 2), (6, 32)))

        self.assertEqual(tree2, False)

    def test_resulting_wrong_player(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        player = "red"
        player2 = "brown"
        state = GameState(board, [player, player2])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        tree2 = tree.resulting_state((player2, (1, 2), (6, 32)))

        self.assertEqual(tree2, False)

    def test_resulting_invalid_move(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        tree2 = tree.resulting_state((player, (6, 32)))

        self.assertEqual(tree2, False)


class TestGameTreeGetChildren(unittest.TestCase):

    def test_regular_behavior_get_children(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        children = tree.get_children()
        moves = list(children.keys())
        moves.sort()

        self.assertEqual([(player, (1, 2), (0, 2)), (player, (1, 2), (2, 2))], moves)

        # ------- check child 1
        first_move_board = [[1, 1, 1], [1, 1, 0], [1, 1, 1]]
        first_move_players = [player]
        first_move_penguin_positions = {'red': [(0, 2)]}
        first_move_turn = 0
        first_move_score = {'red': 1}
        first_move_state = (first_move_board, first_move_players,
                            first_move_penguin_positions, first_move_turn, first_move_score)
        self.assertEqual(first_move_state, children[moves[0]].get_current_state().get_game_state())

        # -------- check child 2
        second_move_board = [[1, 1, 1], [1, 1, 0], [1, 1, 1]]
        second_move_players = [player]
        second_move_penguin_positions = {'red': [(2, 2)]}
        second_move_turn = 0
        second_move_score = {'red': 1}
        second_move_state = (second_move_board, second_move_players,
                             second_move_penguin_positions, second_move_turn, second_move_score)
        self.assertEqual(second_move_state, children[moves[1]].get_current_state().get_game_state())

    def test_no_moves_game_over_get_children(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        board.add_hole((0, 2))
        board.add_hole((2, 2))
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        children = tree.get_children()

        self.assertEqual({}, children)

    def test_no_moves_not_game_over_get_children(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        board.add_hole((0, 2))
        board.add_hole((2, 2))
        player = "red"
        player2 = "black"
        state = GameState(board, [player, player2])
        state.place_penguin(player, (1, 2))
        state.place_penguin(player2, (1, 0))
        tree = GameTree(state)
        children = tree.get_children()
        moves = list(children.keys())
        moves.sort()

        self.assertEqual([(player, False)], moves)

        first_move_board = [[1, 1, 0], [1, 1, 1], [1, 1, 0]]
        first_move_players = [player, player2]
        first_move_penguin_positions = {'red': [(1, 2)], 'black': [(1, 0)]}
        first_move_turn = 1
        first_move_score = {'red': 0, 'black': 0}
        first_move_state = (first_move_board, first_move_players,
                            first_move_penguin_positions, first_move_turn, first_move_score)
        self.assertEqual(first_move_state, children[moves[0]].get_current_state().get_game_state())


class TestGameTreeApply(unittest.TestCase):

    def heuristic(self, gametree):
        scores = gametree.get_current_state().get_game_state()[4]
        return scores['red']

    def test_apply_regular(self):

        board = Board(3, 3)
        board.make_uniform_board(1)
        board.set_fish(5, (0, 2))
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        results = tree.apply(self.heuristic)
        answer = {(player, (1, 2), (0, 2)): 1, (player, (1, 2), (2, 2)): 1}
        self.assertEqual(results, answer)


    def test_apply_no_children(self):
        board = Board(3, 3)
        board.make_uniform_board(1)
        board.add_hole((0, 2))
        board.add_hole((2, 2))
        player = "red"
        state = GameState(board, [player])
        state.place_penguin(player, (1, 2))
        tree = GameTree(state)
        results = tree.apply(self.heuristic)
        answer = {}
        self.assertEqual(results, answer)




if __name__ == '__main__':
    unittest.main()
