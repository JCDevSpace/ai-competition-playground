import sys

sys.path.append('..')
import unittest

from state import GameState
from board import Board
from Model.Player import Player


class TestGameStateCurrentPlayer(unittest.TestCase):

    def test_get_current_player_in_order(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        self.assertEqual(player1, gs.get_current_player())

    def test_get_current_player_out_of_order(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player2, player1], b)
        self.assertEqual(player1, gs.get_current_player())


class TestGameStatePlacePenguin(unittest.TestCase):

    def test_place_regular(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: set(), player2: set()}, gs.get_game_state()[2])

        gs.place_penguin(player1, (1, 1))

        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: set()}, gs.get_game_state()[2])

    def test_place_out_of_bounds(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: set(), player2: set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (-1, 1))

    def test_place_on_hole(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: set(), player2: set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (1, 0))

    def test_place_on_penguin(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: set(), player2: set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (0, 2))


class TestGameStateMovePenguin(unittest.TestCase):

    def test_move_penguin_valid(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: set()}, gs.get_game_state()[2])

        gs.move_penguin(player1, (1, 1), (0, 1))

        self.assertEqual([[1, 0, 0], [-1, -1, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: {(0, 1)}, player2: set()}, gs.get_game_state()[2])

    def test_move_penguin_not_valid_movement(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (0, 0))

    def test_move_penguin_into_hole(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (2, 1))

    def test_move_penguin_into_penguin(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (0, 2))


class TestGameStateGameOver(unittest.TestCase):
    def test_game_over_false(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: set()}, gs.get_game_state()[2])
        self.assertFalse(gs.game_over())

    def test_game_over_one_penguin_cannot(self):
        """
        1   2   -1      1    2   -1
          -1  2  0  ->    -1   0    0     (2, 2) bottom right has no valid moves
        -1  -1  4      -1   -1   0
        """
        b = Board(3, 3, [[1, 2, -1], [-1, 2, 0], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        gs.place_penguin(player2, (2, 2))
        self.assertEqual([[1, 2, -1], [-1, 0, 0], [-1, -1, 0]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: {(2, 2)}}, gs.get_game_state()[2])
        self.assertFalse(gs.has_moves_left(player2))
        self.assertFalse(gs.game_over())

    def test_game_over_true(self):
        """
        -1   -1   -1      -1  -1   -1
          -1  2  -1  ->     -1   0    -1     (1, 1) center has no valid moves
        -1  -1  -1      -1   -1   -1            and since its the only penguin, game is over
        """
        b = Board(3, 3, [[-1, -1, -1], [-1, 2, -1], [-1, -1, -1]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[-1, -1, -1], [-1, 0, -1], [-1, -1, -1]], gs.get_game_state()[0])
        self.assertEqual({player1: {(1, 1)}, player2: set()}, gs.get_game_state()[2])
        self.assertTrue(gs.game_over())


class TestGameStateHasMovesLeft(unittest.TestCase):
    def has_moves_left_false(self):
        pass



if __name__ == '__main__':
    unittest.main()
