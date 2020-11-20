import sys
import unittest
from Common.state import GameState
from Common.board import Board
from Player.player import Player as AIPlayer
from Player.strategy import Strategy


class AIPlayerTestSetState(unittest.TestCase):
    
    def testSetStateCheckState(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState(b, ["red"])

        aiplayer = AIPlayer(Strategy(), 10)

        gs_state = gs.get_game_state()
        aiplayer.set_state(gs_state)
        self.assertEqual(gs_state, aiplayer.state.get_game_state())

class AIPlayerTestGetPlacement(unittest.TestCase):

    def testNoChangeBoard(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState(b, ["red", "brown"])

        aiplayer1 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer1.set_state(gs_state)
        aiplayer1.set_color('brown')

        self.assertEqual(aiplayer1.get_placement(), ('brown', (0, 0)))

    def testHoleBoard(self):
        board = [[0, 0, 0], [0, 0, 0], [0, 4, 0]]
        b = Board(3, 3, layout=board)
        gs = GameState(b, ["red", "brown"])

        aiplayer2 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer2.set_state(gs_state)
        aiplayer2.set_color('brown')

        self.assertEqual(aiplayer2.get_placement(), ('brown', (2, 1)))

    def testPenguinyBoard(self):
        board = [[1, 2, 3], [0, 2, 5], [2, 4, 0]]
        b = Board(3, 3, layout=board)
        player1 = "red"
        player2 = "brown"
        gs = GameState(b, [player1, player2],
                       penguin_positions={player1: [(0, 0), (0, 1), (0, 2)], player2: [(1, 0), (1, 1), (1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_placement(), ('brown', (2, 0)))

    def testFullBoard(self):
        board = [[1, 2, 3], [0, 2, 5], [0, 0, 0]]
        b = Board(3, 3, layout=board)
        player1 = "red"
        player2 = "brown"
        gs = GameState(b, [player1, player2],
                       penguin_positions={player1: [(0, 0), (0, 1), (0, 2)], player2: [(1, 0), (1, 1), (1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        with self.assertRaises(ValueError):
            aiplayer3.get_placement()
class AIPlayerTestGetMove(unittest.TestCase):

    def testBasicMove(self):
        board = [[1, 0, 0], [1, 0, 5], [1, 4, 0]]
        b = Board(3, 3, layout=board)
        player1 = "brown"
        player2 = "red"
        gs = GameState(b, [player1, player2],
                       penguin_positions={player1: [(0, 0)], player2: [(1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_move(), (player1, (0, 0), (2, 1)))

    def testAnotherMove(self):
        board = [[2, 0, 4], [1, 2, 2], [1, 4, 0]]
        b = Board(3, 3, layout=board)
        player1 = "brown"
        player2 = "red"
        gs = GameState(b, [player1, player2],
                       penguin_positions={player1: [(1, 1)], player2: [(1, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_move(), (player1, (1, 1), (2, 1)))

    def testNoMoves(self):
        board = [[2, 0, 4], [0, 0, 0], [0, 0, 4]]
        b = Board(3, 3, layout=board)
        player1 = "brown"
        player2 = "red"
        gs = GameState(b, [player1, player2],
                       penguin_positions={player1: [(0, 0)], player2: [(0, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')

        self.assertEqual(aiplayer3.get_move(), (player1, False))

    def testGameOver(self):
        board = [[2, 0, 4], [0, 0, 0], [0, 0, 0]]
        b = Board(3, 3, layout=board)
        player1 = "red"
        player2 = "brown"
        gs = GameState(b, [player1, player2],
                       penguin_positions={player2: [(0, 0)], player1: [(0, 2)]})

        aiplayer3 = AIPlayer(Strategy, 3)
        gs_state = gs.get_game_state()
        aiplayer3.set_state(gs_state)
        aiplayer3.set_color('brown')
        with self.assertRaises(ValueError):
            aiplayer3.get_move()


if __name__ == '__main__':
    unittest.main()
