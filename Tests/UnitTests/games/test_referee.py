from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from Game.Admin.referee import Referee
from Game.Common.util import generate_players, load_config

class TestRefereeCheckerGames(unittest.TestCase):
    def setUp(self):
        game_config = load_config("default_checker.yaml")
        self.test_ref = Referee(game_config, generate_players(2, 1))

    def test_full_game(self):
        winners, kicked = self.test_ref.run_game()
        self.assertEqual(len(winners), 1)
        self.assertEqual(len(kicked), 0)


class TestRefereeFishGames(unittest.TestCase):
    def setUp(self):
        game_config = load_config("default_fish.yaml")
        self.test_ref = Referee(game_config, generate_players(2, 1))

    def test_full_game(self):
        winners, kicked = self.test_ref.run_game()
        self.assertEqual(len(winners), 1)
        self.assertEqual(len(kicked), 0)


if __name__ == "__main__":
    unittest.main()