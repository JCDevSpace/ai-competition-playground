import unittest
from Player.strategy import Strategy
from Player.player import Player
from Admin.referee import Referee
from Admin.manager import Manager

def generate_players(count):
    players = []
    for age in range(count):
        players.append(Player(Strategy, age, depth=1))

    return players

class TestManagerAssignGroups(unittest.TestCase):
    def test_bad_assign(self):
        players = generate_players(1)
        manager = Manager(players)

        with self.assertRaises(ValueError):
            manager.game_assignment()

    def test_assign_2_players(self):
        players = generate_players(2)
        manager = Manager(players)

        groups = manager.game_assignment()

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 2)

    def test_assign_3_players(self):
        players = generate_players(3)
        manager = Manager(players)

        groups = manager.game_assignment()

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 3)

    def test_assign_4_players(self):
        players = generate_players(4)
        manager = Manager(players)

        groups = manager.game_assignment()

        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 4)


    def test_assign_5_players(self):
        players = generate_players(5)
        manager = Manager(players)

        groups = manager.game_assignment()

        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[0]), 3)
        self.assertEqual(len(groups[1]), 2)


    def test_assign_9_players(self):
        players = generate_players(9)
        manager = Manager(players)

        groups = manager.game_assignment()

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

    def send_message(self, result):
        return False


class TestManagerInformResults(unittest.TestCase):
    def test_inform_results(self):
        winning_players = generate_players(2)
        losing_players = generate_players(2)

        manager = Manager(winning_players)
        manager.knocked_players = losing_players

        manager.inform_tournament_results()

        for player in winning_players:
            self.assertTrue(player.winner)
            self.assertFalse(player.in_tournament)

        for player in losing_players:
            self.assertFalse(player.winner)
            self.assertFalse(player.in_tournament)

    def test_inform_results_winner_false(self):
        winning_players = generate_players(3)
        losing_players = generate_players(2)
        stupid_winner = MockPlayer()
        winning_players[1] = stupid_winner

        manager = Manager(winning_players)
        manager.knocked_players = losing_players

        manager.inform_tournament_results()

        for index, player in enumerate(winning_players):
            if index != 1:
                self.assertTrue(player.winner)
                self.assertFalse(player.in_tournament)

        for player in losing_players:
            self.assertFalse(player.winner)
            self.assertFalse(player.in_tournament)

        # the mock player gets marked as a loser
        self.assertTrue(stupid_winner not in manager.active_players)
        self.assertTrue(stupid_winner in manager.knocked_players)



class TestManagerRunOneRound(unittest.TestCase):
    def test_run_one_round(self):
        players = generate_players(6)
        manager = Manager(players)
        groups = manager.game_assignment()

        manager.run_tournament_round(groups)

        self.assertEqual(manager.active_players[0].get_age(), 0)
        self.assertEqual(manager.active_players[1].get_age(), 3)
        self.assertEqual(manager.active_players[2].get_age(), 4)

        self.assertEqual(manager.knocked_players[0].get_age(), 1)
        self.assertEqual(manager.knocked_players[1].get_age(), 2)
        self.assertEqual(manager.knocked_players[2].get_age(), 5)


class TestManagerRunTournament(unittest.TestCase):
    def test_whole_tournament_one_winner(self):
        players = generate_players(9)
        manager = Manager(players)

        winners, losers = manager.run_tournament()

        self.assertEqual(len(winners), 1)
        self.assertEqual(len(losers), 8)

    def test_whole_tournament_multiple_winners(self):
        players = generate_players(8)
        manager = Manager(players, rows=2, cols=4)

        winners, losers = manager.run_tournament()

        self.assertEqual(len(winners), 8)
        self.assertEqual(len(losers), 0)

if __name__ == '__main__':
    unittest.main()
