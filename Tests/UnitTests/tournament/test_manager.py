from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from asyncio import run
from Game.Common.util import generate_players
from Game.Admin.manager import Manager


class TestManagerRunTournament(unittest.TestCase):
    def test_smart_players(self):
        test_manager = Manager(generate_players(3,1))
        winners, losers, kicked = run(test_manager.run_tournament())
        print("{} winners, {} loser, {} kicked".format(len(winners), len(losers), len(kicked)))

    def test_dumb_players(self):
        test_manager = Manager(generate_players(3,2))
        winners, losers, kicked = run(test_manager.run_tournament())
        print("{} winners, {} loser, {} kicked".format(len(winners), len(losers), len(kicked)))

if __name__ == "__main__":
    unittest.main()