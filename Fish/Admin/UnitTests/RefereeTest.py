import unittest
from Player.strategy import Strategy
from Player.player import Player as AIPlayer
from Admin.referee import Referee

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
        ref.assign_colors()
        ref.set_initial_states()
        self.assertEqual(ref.kicked_players, [])
        player1_data = "red"
        ref.kick_player(player1_data)
        self.assertEqual(ref.kicked_players, [player1_data])

    def testKickOpensSquareAgain(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (0, 0)))
        ref.perform_placement((player2_data, (1, 0)))

        self.assertEqual(ref.game_state.placable_position((0, 0)), False)
        ref.kick_player(player1_data)
        self.assertEqual(ref.game_state.placable_position((0, 0)), True)

class TestRefereePlacement(unittest.TestCase):

    def testBasicValidPlacement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (0, 0)))
        self.assertEqual(ref.game_state.penguin_positions[player1_data], [(0, 0)])

    def testBasicInValidPlacement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (-1, 0)))
        self.assertEqual(ref.is_kicked('red'), True)

    def testBasicInValidPlacement2(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (0, 0)))
        ref.perform_placement((player2_data, (0, 0)))
        self.assertEqual(ref.is_kicked('brown'), True)

    def testOutofOrderPlacement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        ref.perform_placement((player1_data, (0, 0)))
        ref.perform_placement((player1_data, (1, 1)))
        self.assertEqual(ref.is_kicked('red'), True)


class TestRefereeMakeMove(unittest.TestCase):

    def testBasicValidMove(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (0, 0)))
        ref.perform_placement((player2_data, (9, 9)))
        ref.perform_placement((player1_data, (8, 9)))
        ref.perform_placement((player2_data, (0, 1)))
        ref.perform_placement((player1_data, (9, 8)))
        ref.perform_placement((player2_data, (8, 8)))
        ref.perform_placement((player1_data, (7, 8)))
        ref.perform_placement((player2_data, (7, 9)))

        self.assertEqual(ref.get_gamephase(), 'movement')
        move = (player1_data, (0, 0), (1, 0))
        ref.perform_move(move)

        self.assertEqual(ref.is_kicked('red'), False)
        self.assertEqual(ref.game_state.penguin_positions[player1_data],
                         [(1, 0), (8, 9), (9, 8), (7, 8)])

    def testOutOfOrderTurn(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (0, 0)))
        ref.perform_placement((player2_data, (9, 9)))
        ref.perform_placement((player1_data, (8, 9)))
        ref.perform_placement((player2_data, (0, 1)))
        ref.perform_placement((player1_data, (9, 8)))
        ref.perform_placement((player2_data, (8, 8)))
        ref.perform_placement((player1_data, (7, 8)))
        ref.perform_placement((player2_data, (7, 9)))

        self.assertEqual(ref.get_gamephase(), 'movement')
        move = (player1_data, (0, 0), (1, 0))
        move2 = (player1_data, (1, 0), (2, 1))
        ref.perform_move(move)
        ref.perform_move(move2)

        self.assertEqual(ref.is_kicked('red'), True)

    def testWrongPenguin(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (0, 0)))
        ref.perform_placement((player2_data, (9, 9)))
        ref.perform_placement((player1_data, (8, 9)))
        ref.perform_placement((player2_data, (0, 1)))
        ref.perform_placement((player1_data, (9, 8)))
        ref.perform_placement((player2_data, (8, 8)))
        ref.perform_placement((player1_data, (7, 8)))
        ref.perform_placement((player2_data, (7, 9)))

        self.assertEqual(ref.get_gamephase(), 'movement')
        move = (player1_data, (7, 9), (5, 9))
        ref.perform_move(move)
        self.assertEqual(ref.is_kicked('red'), True)

    def testInvalidMovement(self):
        player1 = AIPlayer(Strategy, 3)
        player2 = AIPlayer(Strategy, 67)
        ref = Referee(rows=10, cols=10, players=[player1, player2])
        ref.assign_colors()
        ref.set_initial_states()
        player1_data = "red"
        player2_data = "brown"
        ref.perform_placement((player1_data, (0, 0)))
        ref.perform_placement((player2_data, (9, 9)))
        ref.perform_placement((player1_data, (8, 9)))
        ref.perform_placement((player2_data, (0, 1)))
        ref.perform_placement((player1_data, (9, 8)))
        ref.perform_placement((player2_data, (8, 8)))
        ref.perform_placement((player1_data, (7, 8)))
        ref.perform_placement((player2_data, (7, 9)))

        self.assertEqual(ref.get_gamephase(), 'movement')
        move = (player1_data, (0, 0), (3, 0))
        ref.perform_move(move)
        self.assertEqual(ref.is_kicked('red'), True)




if __name__ == '__main__':
    unittest.main()
