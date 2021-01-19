from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from Game.Common.util import generate_players
from Game.Admin.manager import Manager


class TestManagerRunTournament(unittest.TestCase):
    def setUp(self):
        self.test_manager = Manager(generate_players(11,1))

    def test_full_tournament(self):
        winners, losers, kicked = self.test_manager.run_tournament()
        print("{} winners, {} loser, {} kicked".format(len(winners), len(losers), len(kicked)))


if __name__ == "__main__":
    unittest.main()