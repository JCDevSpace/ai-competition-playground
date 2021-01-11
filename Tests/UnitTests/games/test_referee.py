from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
from Game.Admin.referee import Referee
from Game.Player.minimax_player import MinimaxPlayer

def generate_players(n, d):
        """Generates the specified number of MinimaxPlayer with the specified search depth of 2 for testing.

        Args:
            n (int): a positive integer
        """
        players = [None] * n
    
        for i in range(n):
            players[i] = MinimaxPlayer(depth=d, id=i)

        return players


class TestRefereeCheckerGames(unittest.TestCase):
    def setUp(self):
        self.test_ref = Referee("checker", generate_players(2, 2))

    def test_full_game(self):
        winners, kicked = self.test_ref.run_game()
        self.assertEqual(len(winners), 1)
        self.assertEqual(len(kicked), 0)


class TestRefereeFishGames(unittest.TestCase):
    def setUp(self):
        self.test_ref = Referee("fish", generate_players(4, 1))

    def test_full_game(self):
        winners, kicked = self.test_ref.run_game()
        self.assertEqual(len(winners), 1)
        self.assertEqual(len(kicked), 0)



if __name__ == "__main__":
    unittest.main()