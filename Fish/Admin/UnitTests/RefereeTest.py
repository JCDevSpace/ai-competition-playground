import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

import unittest
from time import sleep
from Fish.Player.strategy import Strategy
from Fish.Player.player import Player as AIPlayer
from Fish.Admin.referee import Referee
from Fish.Admin.game_visualizer import GameVisualizer

class TestRefereeInitStandard(unittest.TestCase):

    def test_referee_init_rows_cols_big(self):
        r = Referee(rows=10, cols=100, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])
        # Seems like a nonsense test but is asserting that the constructor is valid
        self.assertEqual(True, True)

    def test_referee_init_rows_cols_regular(self):
        r = Referee(rows=5, cols=5, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])
        # Seems like a nonsense test but is asserting that the constructor is valid
        self.assertEqual(True, True)

    def test_referee_specific(self):
        r = Referee(rows=3, cols=3, specific_holes=[(2, 2)],
                    players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])
        self.assertEqual(True, True)

    def test_referee_min_holes(self):
        r = Referee(rows=3, cols=3, min_holes=1,
                    players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])
        self.assertEqual(True, True)

    def test_referee_min_one_fish(self):
        r = Referee(rows=3, cols=3, min_one_fish=8,
                    players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])
        self.assertEqual(True, True)

    def test_referee_min_holes_and_fish(self):
        r = Referee(rows=3, cols=3, min_holes=1, min_one_fish=4,
                    players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])
        self.assertEqual(True, True)

    def test_referee_min_holes_and_fish_and_specific(self):
        r = Referee(rows=3, cols=3, min_holes=1, min_one_fish=4,
                    specific_holes=[(0, 0)],
                    players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])
        self.assertEqual(True, True)


class TestRefereeInitError(unittest.TestCase):

    def test_referee_init_row_too_small(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=0, cols=100, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_col_too_small(self):
        with self.assertRaises(ValueError):
            x = Referee(cols=0, rows=100, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_missing_info(self):
        with self.assertRaises(ValueError):
            # missing uniform fish number
            x = Referee(uniform=True,rows=10, cols=10, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_too_many_conditions(self):
        with self.assertRaises(ValueError):
            x = Referee(uniform=True, min_holes=10, rows=10, cols=10, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_too_many_conditions_2(self):
        with self.assertRaises(ValueError):
            x = Referee(uniform=True, min_one_fish=10, rows=10, cols=10, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_too_many_specified(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=2, cols=2, min_holes=3, min_one_fish=2, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_too_many_specified_specific(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=2, cols=2, min_holes=1, min_one_fish=2, specific_holes=[(0, 0), (0, 1), (1, 0)],
                        players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_too_few_squares_for_penguins(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=2, cols=2, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])

    def test_referee_init_too_few_squares_for_penguins_holes(self):
        with self.assertRaises(ValueError):
            x = Referee(rows=10, cols=10, min_holes=93, players=[AIPlayer(Strategy, 2), AIPlayer(Strategy, 4)])


class TestRefereeKickPlayer(unittest.TestCase):
    def testkickone(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        self.assertEqual(ref.kicked_players, [])
        ref.kick_player(player1.assigned_color())
        self.assertEqual(ref.kicked_players, [player1.assigned_color()])

    def testKickOpensSquareAgain(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.perform_placement((player1.assigned_color(), (0, 0)))
        ref.perform_placement((player2.assigned_color(), (1, 0)))

        self.assertFalse(ref.game_state.placable_position((0, 0)))
        ref.kick_player(player1.assigned_color())
        self.assertTrue(ref.game_state.placable_position((0, 0)))

class TestRefereePlacement(unittest.TestCase):

    def testBasicValidPlacement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        self.assertTrue(ref.perform_placement((player1.assigned_color(), (0, 0))))
        self.assertEqual(ref.game_state.penguin_positions[player1.assigned_color()], [(0, 0)])

    def testBasicInValidPlacement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        self.assertFalse(ref.perform_placement((player1.assigned_color(), (-1, 0))))

    def testBasicInValidPlacement2(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.perform_placement((player1.assigned_color(), (0, 0)))
        self.assertFalse(ref.perform_placement((player2.assigned_color(), (0, 0))))

    def testOutofOrderPlacement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        self.assertTrue(ref.perform_placement((player1.assigned_color(), (0, 0))))
        self.assertFalse(ref.perform_placement((player1.assigned_color(), (1, 1))))

    def testTimedOutPlacementResp(self):
        player1 = AIPlayer(Strategy, 3, depth=3)
        player2 = AIPlayer(Strategy, 67)
        bad_player = TimeoutMockPlayer()

        ref = Referee(rows=4, cols=4, players=[player1, player2, bad_player])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.run_phase(ref.PLACEMENT, ref.perform_placement)

        self.assertTrue(ref.is_kicked(bad_player.assigned_color()))
        self.assertTrue(bad_player.kicked)

class TestRefereeMakeMove(unittest.TestCase):

    def testBasicValidMove(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.run_phase(ref.PLACEMENT, ref.perform_placement)

        self.assertEqual(ref.get_gamephase(), ref.MOVEMENT)
        move = (player1.assigned_color(), (0, 0), (1, 0))
        self.assertTrue(ref.perform_move(move))
        self.assertEqual(ref.game_state.penguin_positions[player1.assigned_color()],
                         [(1, 0), (0, 2), (0, 4), (0, 6)])

    def testOutOfOrderTurn(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.run_phase(ref.PLACEMENT, ref.perform_placement)

        self.assertEqual(ref.get_gamephase(), ref.MOVEMENT)
        move = (player1.assigned_color(), (0, 0), (1, 0))
        move2 = (player1.assigned_color(), (1, 0), (2, 1))
        self.assertTrue(ref.perform_move(move))
        self.assertFalse(ref.perform_move(move2))

    def testWrongPenguin(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.run_phase(ref.PLACEMENT, ref.perform_placement)

        self.assertEqual(ref.get_gamephase(), ref.MOVEMENT)
        move = (player1.assigned_color(), (7, 9), (5, 9))
        self.assertFalse(ref.perform_move(move))

    def testInvalidMovement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.run_phase(ref.PLACEMENT, ref.perform_placement)

        self.assertEqual(ref.get_gamephase(), ref.MOVEMENT)
        move = (player1.assigned_color(), (0, 0), (3, 0))
        self.assertFalse(ref.perform_move(move))

    def testTimedOutMovementResp(self):
        player1 = AIPlayer(Strategy, 3, depth=3)
        player2 = AIPlayer(Strategy, 67)
        bad_player = TimeoutMockPlayer()

        ref = Referee(rows=4, cols=4, players=[player1, player2, bad_player])
        ref.update_color_assignments()
        ref.update_initial_states()
        ref.run_phase(ref.PLACEMENT, ref.perform_placement)

        self.assertEqual(ref.get_gamephase(), ref.MOVEMENT)

        ref.run_phase(ref.MOVEMENT, ref.perform_move)
        self.assertTrue(ref.is_kicked(bad_player.assigned_color()))
        self.assertTrue(bad_player.kicked)

class TestRefereeCompleteGame(unittest.TestCase):

    def testTwoPlayerCompleteGame(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=5, cols=5, players=[player1, player2])
        winners = ref.run_game()
        winner_ages = [winner.get_age() for winner in winners]
        self.assertEqual(winner_ages, [67])

    def testTwoPlayerCompleteGame(self):
        players = [
            AIPlayer(Strategy, 19),
            AIPlayer(Strategy, 20),
            AIPlayer(Strategy, 30),
            AIPlayer(Strategy, 67)
        ]
        ref = Referee(rows=4, cols=4, uniform=True, uniform_fish_num=4, players=players)
        winners, _ = ref.run_game()
        winner_info = [(winner.get_age(), winner.assigned_color()) for winner in winners]
        self.assertEqual(winner_info, [(19, 'red'), (20, 'brown'), (30, 'white'), (67, 'black')])


class TimeoutMockPlayer(AIPlayer):

    def __init__(self):
        super().__init__(Strategy, 1)

    def get_placement(self):
        sleep(20)

    def get_move(self):
        sleep(20)

if __name__ == '__main__':
    unittest.main()
