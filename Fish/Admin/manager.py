from Fish.Common.message import Message
from Fish.Admin.referee import Referee

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
    # 
    #
    def __init__(self, players, rows=DEFAULT_ROWS, cols=DEFAULT_COLS):
        self.active_players = sorted(players, key = lambda player : player.get_age())
        self.knocked_players = []
        self.rows = rows
        self.cols = cols

    # Runs a fish tournament for the players in self.active_players
    # The tournament runs in rounds. Each round players are assigned to groups to
    # play games of fish and only the winners of these games advance to the next round.
    # The tournament is over once there are not enough active players for another game or
    # there is a round where no new players are knocked out of the tournament.
    # Returns the winners and losers of the tournament
    # Void -> List[Player], List[Player]
    def run_tournament(self):
        self.inform_tournament_start()

        previous_winner_count = None
        while len(self.active_players) >= MIN_PLAYERS_PER_GAME:

            player_groups = self.game_assignment()
            self.run_tournament_round(player_groups)

            if previous_winner_count == len(self.active_players):
                break
    
            previous_winner_count = len(self.active_players)

        self.inform_tournament_results()

        return self.active_players, self.knocked_players
        
    # Splits the active players into groups by first creating as many
    # games of maximum size as possible. If at the end there are not enough
    # players left to make a final group, players from last group of max size are
    # removed to make the final group large enough.
    # Void -> List[List[Player]]
    # raises ValueError if there are less than the minimum amount of active players
    def game_assignment(self):
        if len(self.active_players) < MIN_PLAYERS_PER_GAME:
            raise ValueError("trying to assign players to groups when there are not enough players")
        
        groups = []
        # remove the max number of players per game until we cant
        while len(self.active_players) >= MAX_PLAYERS_PER_GAME:
            group = []
            for _ in range(MAX_PLAYERS_PER_GAME):
                group.append(self.active_players.pop(0))

            groups.append(group)

        # if there are players left, backtrack until there are enough to make a group
        if len(self.active_players) > 0:
            while len(self.active_players) < MIN_PLAYERS_PER_GAME:
                previous_group = groups[-1]
                backtracked_player = previous_group.pop()
                self.active_players.insert(0, backtracked_player)
                
            group = []
            while len(self.active_players) > 0:
                group.append(self.active_players.pop(0))
            groups.append(group)

        return groups

    # Runs the corresponding games for players assigned to each of the groups
    # and gathers information on the winner and loser for each of the group
    # games and allow the winners to move on to the next tournament round
    # if the tournament is not over.
    # list(list(Players)) -> Void
    def run_tournament_round(self, player_groups):
        for group in player_groups:
            winners = Referee(group, self.rows, self.cols, DEFAULT_UNIFORM, DEFAULT_UNIFORM_COUNT).run_game()

            for player in group:
                if player in winners:
                    self.active_players.append(player)
                else:
                    self.knocked_players.append(player)


    # Informs all the players in the tournament that it's starting
    # Void -> Void
    def inform_tournament_start(self):
        for player in self.active_players:
            response = self.query_player(player, Message.generate_notify_start())
            # do something with the ack?

    # Informs all players in the tournament whether or not they have won,
    # for any player that didn't properly acknowledge the win, they will become 
    # losers.
    # Void -> Void
    def inform_tournament_results(self):
        index = 0
        while index < len(self.active_players):
            response = self.query_player(self.active_players[index], Message.generate_notify_results(True))
            if not response:
                stupid_loser = self.active_players.pop(index)
                self.knocked_players.append(stupid_loser)
            else:
                index += 1
                
        for player in self.knocked_players:
            response = self.query_player(player, Message.generate_notify_results(False))
            
    
    # Sends a message to a player object and safely
    # gets their response
    # Player, Message -> Response
    def query_player(self, player, message):
        # TODO: add timeout around this call
        try:
            response = player.send_message(message)
        except:
            response = False

        return response

    #def add_observers(self, observers):
    #    pass
