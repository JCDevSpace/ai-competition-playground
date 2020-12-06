import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

from Fish.Admin.referee import Referee
from Fish.Common.util import safe_execution

MIN_PLAYERS_PER_GAME = 2
MAX_PLAYERS_PER_GAME = 4
DEFAULT_ROWS = 5
DEFAULT_COLS = 5
DEFAULT_UNIFORM = True
DEFAULT_UNIFORM_COUNT = 3


# The manager object runs an entire tournament of the Fish game
# given a list of players, the list of players don't have to be in any
# particular order

# At the start of a tournament, the manager informs all the players that the
# Tournament will be started.

# The tournament uses a knock-out elimination system. The top finisher(s) of every game of round n move on to round n+1. The tournament ends when two tournament rounds of games in a row produce the exact same winners, when there are too few players for a single game, or when the number of participants has become small enough to run a single final game. In both cases, the surviving players will be the tournament winners.

# The allocation of players to games works as follows. The manager starts by assigning them to games with the maximal number of participants permitted in ascending order of age. Once the number of remaining players drops below the maximal number and can’t form a game, the manager backtracks by one game and tries games of size one less than the maximal number and so on until all players are assigned.

# When the tournament is over, the manager informs all remaining active players whether they won or lost. Winners that fail to accept this message become losers.


class Manager:
    # Constructs an instance of the tournament manager to manage the tournament for
    # the given list of players
    def __init__(self, players, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, fish=DEFAULT_UNIFORM_COUNT, observers=[]):
        self.players = players
        self.rows = rows
        self.cols = cols
        self.fish = fish

        self.observers = observers

        self.kicked_players = []
        self.losers = []

    # Runs a fish tournament for the players in self.players
    # The tournament runs in rounds. Each round players are assigned to groups to
    # play games of fish and only the winners of these games advance to the next round.
    # The tournament is over once there are not enough active players for another game or
    # there is a round where no new players are knocked out of the tournament.
    # Returns the number of winners and losers + knocked out players of the tournament
    # Void -> Int, Int
    def run_tournament(self):
        remaining_players = self.inform_tournament_start()

        winners, losers = self.run_game_rounds(remaining_players)

        final_winners = self.inform_tournament_results(winners, losers)

        return final_winners, self.kicked_players
        
    # Run the rounds of games until the tournament winners are decided with the given
    # list of players and returns the final winner and losers.
    # List[Players] -> (Int, Int)
    def run_game_rounds(self, active_players):
        active_players = sorted(self.players, key = lambda player : player.get_age())

        previous_winner_count = 0
        while len(active_players) >= MIN_PLAYERS_PER_GAME:
            player_groups = self.game_assignment(active_players)

            if len(player_groups) > 1:
                round_winners, round_losers = self.run_games(player_groups)
                
                if previous_winner_count == len(round_winners):
                    return round_winners, round_losers

                self.losers.extend(round_losers)
        
                active_players = sorted(round_winners, key = lambda player : player.get_age())
                previous_winner_count = len(active_players)
            else:
                return self.run_games(player_groups)

    # Consumes given list of players and split them into groups by first creating as many
    # games of maximum size as possible. If at the end there are not enough
    # players left to make a final group, players from last group of max size are
    # removed to make the final group large enough.
    # List[Players] -> List[List[Player]]
    # raises ValueError if there are less than the minimum amount of active players
    def game_assignment(self, players):
        if len(players) < MIN_PLAYERS_PER_GAME:
            raise ValueError("trying to assign players to groups when there are not enough players")
        
        groups = []
        # remove the max number of players per game until we cant
        while len(players) >= MAX_PLAYERS_PER_GAME:
            group = []
            for _ in range(MAX_PLAYERS_PER_GAME):
                group.append(players.pop(0))

            groups.append(group)

        # if there are players left, backtrack until there are enough to make a group
        if len(players) > 0:
            while len(players) < MIN_PLAYERS_PER_GAME:
                previous_group = groups[-1]
                backtracked_player = previous_group.pop()
                players.insert(0, backtracked_player)
                
            group = []
            while len(players) > 0:
                group.append(players.pop(0))
            groups.append(group)

        return groups

    # Runs the one round of games for players assigned to each of the groups
    # and returns the list of all players that won in their respective group
    # as well as the list of all players that lost in their respective group
    # list(list(Players)) -> list(Players)
    def run_games(self, player_groups):
        round_winners = []
        round_losers = []

        for group in player_groups:
            winners, kicked = Referee(group, self.rows, self.cols, DEFAULT_UNIFORM, self.fish, observers=self.observers).run_game()

            self.kicked_players.extend(kicked)

            round_winners.extend(winners)

            round_losers.extend([player for player in group if (player not in winners) and (player not in kicked)])

        return round_winners, round_losers

    # Informs all the players of the start of the tournament
    # Void -> List[Player]
    def inform_tournament_start(self):
        remaining_players = []
        
        for player in self.players:
            ret, exc = safe_execution(player.tournamnent_start_update, timeout=2)
            if exc:
                self.kicked_players.append(player)
            else:
                remaining_players.append(player)

    # Informs the given winner and losers of the tournament, if a winner
    # failed to acknoledge a win, they become losers.
    # List, List -> Void
    def inform_tournament_results(self, winners, losers):
        final_winners = []

        for player in winners:
            ret, exc = safe_execution(player.tournamnent_result_update, [True])
            if exc:
                self.kicked_players.append(player)
            else:
                final_winners.append(player)
                
        for player in losers:
            safe_execution(player.tournamnent_result_update, [False])

        return final_winners
