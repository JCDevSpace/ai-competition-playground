import unittest
from Common.game_tree import GameTree
from Common.board import Board
from Common.state import GameState
from Common.Model.Player import Player
from Player.strategy import Strategy

class TestStrategyGetPlacement(unittest.TestCase):
    def test_first_placement(self):
        board = Board(3, 3)
        board.make_uniform_board(1)

        player = Player(10, "red")
        state = GameState([player], board)

        self.assertEqual((0, 0), Strategy.get_placement(state))


    def test_second_placement(self):
        board = Board(3, 3)
        board.make_uniform_board(1)

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        state = GameState([player1, player2], board)

        state.place_penguin(player1, (0, 0))

        self.assertEqual((0, 1), Strategy.get_placement(state))


    def test_after_several_placements(self):
        board = Board(3, 3)
        board.make_uniform_board(1)

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        player3 = Player(42, "white")
        state = GameState([player1, player2, player3], board)

        state.place_penguin(player1, (0, 0))
        state.place_penguin(player2, (0, 1))
        state.place_penguin(player3, (0, 2))
        state.place_penguin(player1, (1, 0))

        self.assertEqual((1, 1), Strategy.get_placement(state))


    def test_holes(self):
        board = Board(3, 3)
        board.make_uniform_board(1)
        board.add_hole((0, 0))

        player = Player(10, "red")
        state = GameState([player], board)

        self.assertEqual((0, 1), Strategy.get_placement(state))

    def test_no_placement(self):
        board = Board(1, 1)
        board.make_uniform_board(1)
        board.add_hole((0, 0))

        player = Player(10, "red")
        state = GameState([player], board)

        with self.assertRaises(ValueError):
            Strategy.get_placement(state)

class TestStrategyMinimax(unittest.TestCase):
    def test_player_winner(self):
        board = Board(3, 3, [[0, 0, 0], [0, 2, 0], [0, 3, 0]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 1)], player2: [(2, 1)]}
        scores = {player1: 8, player2: 4}
        state = GameState([player1, player2], board, penguins, 0, scores)

        self.assertEqual(8, Strategy.minimax(GameTree(state), player1, 2))


    def test_not_player_winner(self):
        board = Board(3, 3, [[0, 0, 0], [0, 2, 0], [0, 3, 0]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 1)], player2: [(2, 1)]}
        scores = {player1: 4, player2: 8}
        state = GameState([player1, player2], board, penguins, 0, scores)

        self.assertEqual(4, Strategy.minimax(GameTree(state), player1, 2))

    def test_tie(self):
        board = Board(3, 3, [[0, 0, 0], [0, 2, 0], [0, 3, 0]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 1)], player2: [(2, 1)]}
        scores = {player1: 8, player2: 8}
        state = GameState([player1, player2], board, penguins, 0, scores)

        self.assertEqual(8, Strategy.minimax(GameTree(state), player1, 2))

    def test_depth_reached(self):
        board = Board(3, 3, [[1, 0, 1], [0, 2, 1], [0, 3, 0]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 1)], player2: [(2, 1)]}
        scores = {player1: 4, player2: 8}
        state = GameState([player1, player2], board, penguins, 0, scores)

        self.assertEqual(4, Strategy.minimax(GameTree(state), player1, 0))

    def test_recur(self):
        board = Board(3, 3, [[1, 0, 1], [0, 2, 1], [0, 3, 0]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 1)], player2: [(2, 1)]}
        scores = {player1: 4, player2: 8}
        state = GameState([player1, player2], board, penguins, 1, scores)

        self.assertEqual(6, Strategy.minimax(GameTree(state), player1, 1))


class TestStrategyGetMove(unittest.TestCase):
    def test_makes_straightforward_move(self):
        board = Board(3, 3, [[4, 1, 1],
                               [3, 2, 1],
                             [1, 1, 1]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 0)], player2: [(2, 2)]}
        scores = {player1: 4, player2: 8}
        state = GameState([player1, player2], board, penguins, 0, scores)

        self.assertEqual((player1, (1, 0), (0, 0)), Strategy.get_move(GameTree(state), 2))

    def test_depth_matters(self):
        board = Board(5, 5, [[0, 0, 4, 0, 1],
                               [0, 1, 1, 1, 3],
                             [0, 0, 0, 1, 1],
                               [3, 0, 1, 1, 3],
                             [0, 3, 3, 3, 1]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 2)], player2: [(4, 4)]}
        scores = {player1: 4, player2: 4}
        state = GameState([player1, player2], board, penguins, 0, scores)

        # when only looking a little ahead moves towards honeypot
        self.assertEqual((player1, (1, 2), (0, 2)), Strategy.get_move(GameTree(state), 2))

        # when looking further ahead doesnt get jebaited
        self.assertEqual((player1, (1, 2), (3, 3)), Strategy.get_move(GameTree(state), 5))

    def test_no_moves_left_for_calling_player(self):
        board = Board(5, 5, [[1, 0, 4, 0, 1],
                               [0, 1, 1, 1, 3],
                             [0, 0, 0, 1, 1],
                               [3, 0, 1, 1, 3],
                             [0, 3, 3, 3, 1]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(0, 0)], player2: [(4, 4)]}
        scores = {player1: 4, player2: 4}
        state = GameState([player1, player2], board, penguins, 0, scores)

        self.assertEqual((player1, False), Strategy.get_move(GameTree(state), 4))

    def test_game_over(self):
        board = Board(3, 3, [[0, 0, 0], [0, 2, 0], [0, 3, 0]])

        player1 = Player(10, "red")
        player2 = Player(12, "brown")
        penguins = {player1: [(1, 1)], player2: [(2, 1)]}
        scores = {player1: 4, player2: 4}
        state = GameState([player1, player2], board, penguins, 0, scores)

        with self.assertRaises(ValueError):
            Strategy.get_move(GameTree(state), 2)


class TestTiebreaker(unittest.TestCase):
    def test_returns_lowest_start_row(self):
        player = Player(10, "red")
        moves = [
          (player, (0, 1) , (1, 1)),
          (player, (1, 1) , (3, 1)),
          (player, (2, 1) , (1, 1))
        ]

        self.assertEqual(moves[0], Strategy.tiebreaker(moves))

    def test_returns_lowest_start_col(self):
        player = Player(10, "red")
        moves = [
          (player, (0, 1) , (1, 1)),
          (player, (0, 2) , (3, 1)),
          (player, (2, 1) , (1, 1))
        ]

        self.assertEqual(moves[0], Strategy.tiebreaker(moves))

    def test_returns_lowest_end_row(self):
        player = Player(10, "red")
        moves = [
          (player, (0, 1) , (1, 1)),
          (player, (0, 1) , (3, 1)),
          (player, (2, 1) , (1, 1))
        ]
        self.assertEqual(moves[0], Strategy.tiebreaker(moves))
