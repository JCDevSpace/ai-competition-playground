import sys
sys.path.append('..')
import unittest

from Model.GameState import GameState
from Model.Board import Board
from Model.Player import Player

class TestGameStateCurrentPlayer(unittest.TestCase):

     def testgetcurrentplayerinorder(self):
         b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
         player1 = Player(10, 'red')
         player2 = Player(15, 'brown')
         gs = GameState([player1, player2], b)
         self.assertEqual(player1, gs.get_current_player())

     def testgetcurrentplayeroutoforder(self):
         b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
         player1 = Player(10, 'red')
         player2 = Player(15, 'brown')
         gs = GameState([player2, player1], b)
         self.assertEqual(player1, gs.get_current_player())


class TestGameStatePlacePenguin(unittest.TestCase):

    def testplaceregular(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set(), player2 : set()}, gs.get_game_state()[2])

        gs.place_penguin(player1, (1, 1))

        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set([(1, 1)]), player2 : set()}, gs.get_game_state()[2])

    def testplaceoutofbounds(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set(), player2 : set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (-1, 1))

    def testplaceonhole(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set(), player2 : set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (1, 0))

    def testplaceonpenguin(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set(), player2 : set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (0, 2))


class TestGameStateMovePenguin(unittest.TestCase):

    def testmovepenguinvalid(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set([(1, 1)]), player2 : set()}, gs.get_game_state()[2])

        gs.move_penguin(player1, (1, 1), (0, 1))

        self.assertEqual([[1, 0, 0], [-1, -1, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set([(0, 1)]), player2 : set()}, gs.get_game_state()[2])

    def testmovepenguinnotvalidmovement(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set([(1, 1)]), player2 : set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (0, 0))

    def testmovepenguinintohole(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set([(1, 1)]), player2 : set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (2, 1))

    def testmovepenguinintopenguin(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = Player(10, 'red')
        player2 = Player(15, 'brown')
        gs = GameState([player1, player2], b)
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 0], [-1, 0, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1 : set([(1, 1)]), player2 : set()}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (0, 2))

    


if __name__ == '__main__':
    unittest.main()
