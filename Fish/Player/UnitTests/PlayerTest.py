import sys
import unittest
from Common.state import GameState
from Common.board import Board
from Common.Model.Player import Player as PlayerDataStore
from Player.player import Player as AIPlayer
from Player.strategy import Strategy


class AIPlayerTestSetState(unittest.TestCase):

    def testSetStateCheckType(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState([PlayerDataStore(10, 'red')], b)

        aiplayer = AIPlayer(Strategy(), 10)
        self.assertEqual(aiplayer.state, None)

        gs_state = gs.get_game_state()
        self.assertEqual(type(gs_state), tuple)
        aiplayer.set_state(gs_state)
        self.assertEqual(type(aiplayer.state), GameState)

    def testSetStateCheckState(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState([PlayerDataStore(10, 'red')], b)

        aiplayer = AIPlayer(Strategy(), 10)

        gs_state = gs.get_game_state()
        aiplayer.set_state(gs_state)
        self.assertEqual(gs_state, aiplayer.state.get_game_state())

class AIPlayerTestMyTurn(unittest.TestCase):

    def testMyTurnHuhEasy(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState([PlayerDataStore(10, 'red')], b)
        aiplayer = AIPlayer(Strategy(), 10)
        gs_state = gs.get_game_state()
        aiplayer.set_state(gs_state)
        aiplayer.set_color('red')

        self.assertEqual(aiplayer.my_turn_huh(), True)

    def testMyTurnHuhMultiple(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState([PlayerDataStore(10, 'red'), PlayerDataStore(3, 'brown')], b)
        aiplayer = AIPlayer(Strategy(), 10)
        gs_state = gs.get_game_state()
        aiplayer.set_state(gs_state)
        aiplayer.set_color('brown')

        self.assertEqual(aiplayer.my_turn_huh(), True)

    def testMyTurnHuhMultipleFalse(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState([PlayerDataStore(10, 'red'), PlayerDataStore(3, 'brown')], b)
        aiplayer = AIPlayer(Strategy(), 10)
        gs_state = gs.get_game_state()
        aiplayer.set_state(gs_state)
        aiplayer.set_color('red')

        self.assertEqual(aiplayer.my_turn_huh(), True)

class AIPlayerTestGetPlacement(unittest.TestCase):

    def testNoChangeBoard(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState([PlayerDataStore(10, 'red'), PlayerDataStore(3, 'brown')], b)

        aiplayer1 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer1.set_state(gs_state)
        aiplayer1.set_color('brown')

        self.assertEqual(aiplayer1.get_placement(), (0, 0))

    def testHoleBoard(self):
        board = [[0, 0, 0], [0, 0, 0], [0, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState([PlayerDataStore(10, 'red'), PlayerDataStore(3, 'brown')], b)

        aiplayer2 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer2.set_state(gs_state)
        aiplayer2.set_color('brown')

        self.assertEqual(aiplayer2.get_placement(), (2, 1))

    def testPenguinyBoard(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        player1 = PlayerDataStore(10, 'red')
        player2 = PlayerDataStore(3, 'brown')
        gs = GameState([player1, player2], b,
                       penguin_positions={player1: [(0, 0), (0, 1), (0, 2)], player2: [(1, 0), (1, 1), (1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_placement(), (2, 0))

    def testFullBoard(self):
        board = [[1, 2, 3], [0, 2, 5], [0, 0, 0]]
        b = Board(3, 3, layout=board)
        player1 = PlayerDataStore(10, 'red')
        player2 = PlayerDataStore(3, 'brown')
        gs = GameState([player1, player2], b,
                       penguin_positions={player1: [(0, 0), (0, 1), (0, 2)], player2: [(1, 0), (1, 1), (1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        with self.assertRaises(ValueError):
            aiplayer3.get_placement()

    def testNoState(self):
        aiplayer3 = AIPlayer(Strategy, 3)
        aiplayer3.set_color('brown')
        with self.assertRaises(ValueError):
            aiplayer3.get_placement()


class AIPlayerTestGetMove(unittest.TestCase):

    def testBasicMove(self):
        board = [[1, 0, 0], [1, 0, 5], [1, 4, 0]]
        b = Board(3, 3, layout=board)
        player1 = PlayerDataStore(10, 'red')
        player2 = PlayerDataStore(3, 'brown')
        gs = GameState([player1, player2], b,
                       penguin_positions={player2: [(0, 0)], player1: [(1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_move(), (player2, (0, 0), (2, 1)))

    def testAnotherMove(self):
        board = [[2, 0, 4], [1, 2, 2], [1, 4, 0]]
        b = Board(3, 3, layout=board)
        player1 = PlayerDataStore(10, 'red')
        player2 = PlayerDataStore(3, 'brown')
        gs = GameState([player1, player2], b,
                       penguin_positions={player2: [(1, 1)], player1: [(1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_move(), (player2, (1, 1), (2, 1)))

    def testNoMoves(self):
        board = [[2, 0, 4], [0, 0, 0], [0, 0, 4]]
        b = Board(3, 3, layout=board)
        player1 = PlayerDataStore(10, 'red')
        player2 = PlayerDataStore(3, 'brown')
        gs = GameState([player1, player2], b,
                       penguin_positions={player2: [(0, 0)], player1: [(0, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_move(), (player2, False))

    def testGameOver(self):
        board = [[2, 0, 4], [0, 0, 0], [0, 0, 0]]
        b = Board(3, 3, layout=board)
        player1 = PlayerDataStore(10, 'red')
        player2 = PlayerDataStore(3, 'brown')
        gs = GameState([player1, player2], b,
                       penguin_positions={player2: [(0, 0)], player1: [(0, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')
        with self.assertRaises(ValueError):
            aiplayer3.get_move()


if __name__ == '__main__':
    unittest.main()
