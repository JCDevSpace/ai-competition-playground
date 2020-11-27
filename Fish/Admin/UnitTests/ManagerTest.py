import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

import unittest
from Fish.Player.strategy import Strategy
from Fish.Player.player import Player
from Fish.Admin.referee import Referee
from Fish.Admin.manager import Manager

def generate_players(count):
    players = []
    for age in range(count):
        players.append(Player(Strategy, age + 5, depth=1))

    return players

class TestManagerAssignGroups(unittest.TestCase):
    def test_bad_assign(self):
        players = generate_players(1)
        manager = Manager(players)

        with self.assertRaises(ValueError):
            manager.game_assignment(players)

    def test_assign_2_players(self):
        players = generate_players(2)
        manager = Manager(players)

        groups = manager.game_assignment(players)

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 2)

    def test_assign_3_players(self):
        players = generate_players(3)
        manager = Manager(players)

        groups = manager.game_assignment(players)

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 3)

    def test_assign_4_players(self):
        players = generate_players(4)
        manager = Manager(players)

        groups = manager.game_assignment(players)

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 4)


    def test_assign_5_players(self):
        players = generate_players(5)
        manager = Manager(players)

        groups = manager.game_assignment(players)

        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[0]), 3)
        self.assertEqual(len(groups[1]), 2)


    def test_assign_9_players(self):
        players = generate_players(9)
        manager = Manager(players)

        groups = manager.game_assignment(players)

        self.assertEqual(len(groups), 3)
        self.assertEqual(len(groups[0]), 4)
        self.assertEqual(len(groups[1]), 3)
        self.assertEqual(len(groups[2]), 2)


class TestManagerInformTournamentStart(unittest.TestCase):
    def test_inform_start(self):
        players = generate_players(4)

        manager = Manager(players)

        manager.inform_tournament_start()

        for player in players:
            self.assertEqual(player.in_tournament, True)


class MockPlayer(Player):
    def __init__(self):
        super().__init__(Strategy, 2)

    def tournamnent_result_update(self, won):
        from time import sleep
        sleep(2)

class TestManagerInformResults(unittest.TestCase):
    def test_inform_results(self):
        winning_players = generate_players(2)
        losing_players = generate_players(2)

        manager = Manager([winning_players, losing_players])

        manager.inform_tournament_results(winning_players, losing_players)

        for player in winning_players:
            self.assertTrue(player.won)
            self.assertFalse(player.in_tournament)

        for player in losing_players:
            self.assertFalse(player.won)
            self.assertFalse(player.in_tournament)

    def test_inform_results_winner_false(self):
        winning_players = generate_players(3)
        losing_players = generate_players(2)
        stupid_winner = MockPlayer()
        winning_players.append(stupid_winner)

        manager = Manager(winning_players)

        final_winners = manager.inform_tournament_results(winning_players, losing_players)

        for player in final_winners:
            self.assertTrue(player.won)
            self.assertFalse(player.in_tournament)

        for player in losing_players:
            self.assertFalse(player.won)
            self.assertFalse(player.in_tournament)

        # the mock player gets marked as a loser
        self.assertTrue(stupid_winner not in final_winners)
        self.assertFalse(stupid_winner.won)

class TestManagerRunOneRound(unittest.TestCase):
    def test_run_one_round(self):
        players = generate_players(6)
        manager = Manager(players)
        groups = manager.game_assignment(players)

        round_winners, round_losers = manager.run_games(groups)

        self.assertEqual([winner.get_age() for winner in round_winners], [5,8,9])
        self.assertEqual([loser.get_age() for loser in round_losers], [6,7,10])


class TestManagerRunTournament(unittest.TestCase):
    def test_whole_tournament_one_winner(self):
        players = generate_players(7)
        smart_player = Player(Strategy, 0)
        players.append(smart_player)

        manager = Manager(players)

        winners = manager.run_tournament()

        self.assertEqual(len(winners), 1)

    def test_whole_tournament_multiple_winners(self):
        players = generate_players(8)
        manager = Manager(players, rows=2, cols=4)

        winners = manager.run_tournament()

        self.assertEqual(len(winners), 8)

if __name__ == '__main__':
    unittest.main()
