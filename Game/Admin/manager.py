from Game.Common.util import safe_execution, load_config
from Game.Admin.referee import Referee
from random import sample


class Manager:
    """
    A Manager is a combination of:
    -list(IPlayer):
        a list of active players still in contest of the tournament
    -list(IPlayer):
        a list of players that already lost in the tournament
    -list(IPlayer):
        a list of kicked players
    -list(IObserver):
        a list of observers that recieves any tournament progress updates

    A Manager is responsible for managing a tournament of board games, hanlding creations of games by assigning groups of players to different referees for individual games then gathering the winners from each game to advance to next rounds. The manager is also responsible for notifying all players and observers of tournament progresses as well as informing each on the start and end result of a tournament.

    The manager loads configuration of tournament from the corresponding configuration files, configuring things like what kind of board games to run, and rules for determining the final winner.

    The tournament uses a knock-out elimination system. The top finisher(s) of every game of round n move on to round n+1. The tournament ends when two tournament rounds of games in a row produce the exact same winners or when there are only the minimum number or less player left.

    The allocation of players to games works as follows. The manager starts by assigning them to games with the maximal number of player permitted randomly. Once the number of remaining players drops below the maximal number and can’t form a game, the manager backtracks by one game and tries games of size one less than the maximal number and so on until all players are assigned.

    At the start of a tournament, the manager informs all the player and observers that a tournament will be started.

    After one rounds of game, the manager informs all player and observers of players who advanced and got knocked out. 

    At the end of the tournament, the manager informs all player and observers the tournament results.

    player who got kicked from game for whatever reason will not be inform of any new information.
    """

    TOURNAMENT_START = 0
    TOURNAMENT_PROGRESS = 1
    TOURNAMENT_END = 2

    def __init__(self, players, observers=None):
        """Initializes a tournament manager with the given players and observers.

        Args:
            players (list(IPlayer)): a list of players
            observers (list(IObserver), optional): a list of observers. Defaults to None.
        """
        self.active_players = players

        if observers:
            self.observers = observers
        else:
            self.observers = []

        self.kicked_players = []
        self.losers = []

        tournament_config = load_config("default_tournament.yaml")
        
        self.min_players = tournament_config["min_players"]

        self.game_rotation = self.setup_rotation(tournament_config["rotation_configs"])

    def setup_rotation(self, config_files):
        """Loads the given configuration files then returns the corresponding game rotation configuration list.

        Args:
            list(str): a list of the game configuration files names 

        Returns:
            list(dict): a list of dict
        """
        rotations = []
        
        for f in config_files:
            game_config = load_config(f)
            rotations.append(game_config)
        
        return rotations
    
    def run_tournament(self):
        """Runs a tournament of board games for the initialized active players.The tournament runs in rounds. Each round players are assigned to groups to play a game and only the winners of the indivual games advance to the next round. The tournament is over either there are only the minimum number or less players left or two round of games produce the same winners.

        Returns:
            triplet(list(IPlayer)): a triplet of lists of players, where the first list is the winners of the tournament and the second players who lost and the last players who got kicked
        """
        self.inform_all(self.TOURNAMENT_START, [[player.get_name() for player in self.active_players]])

        self.run_game_rounds()

        self.inform_all(self.TOURNAMENT_END, [[player.get_name() for player in self.active_players]])

        return self.active_players, self.losers, self.kicked_players

    def run_game_rounds(self):
        """Run the rounds of games with the initial active players until the tournament is over by first assignment player into groups then run the games for each group and and collect all the winners and losers. Winners will automatically advance to the next rounds.
        """
        previous_active_count = 0
        round_count = 0

        while len(self.active_players) > self.min_players \
                and len(self.active_players) != previous_active_count:
            
            game_config = self.game_rotation[round_count % len(self.game_rotation)]

            player_groups = self.assign_groups(game_config["max_players"], game_config["min_players"])

            print("starting {} round".format(game_config["board_type"]))
            self.run_games(player_groups, game_config)

            print("Finished round {} with {} remaining active players, {} loser and {} kicked players".format(round_count, len(self.active_players), len(self.losers), len(self.kicked_players)))

            round_count += 1
    
    def assign_groups(self, max_size, min_size):
        """Assigns active players into groups and returns the group list. Players are assign randomly into groups of max_size first, and if this leaves a number of player less than min_size unassigned, backtracks one group assignment and assigns groups of max_size - 1 and repeat until everyone is assigned in a group.

        Args:
            max_size (int): a positive integer
            min_size (int): a positive integer

        Returns:
            list(list(IPlayer)): a list of lists of players, where the each list of player in assigned in the same group
        """
        unassign_idxs = set(range(len(self.active_players)))
        
        previous_idxs = None
        groups = []
        
        while len(unassign_idxs) >= max_size:
            sample_idxs = sample(unassign_idxs, max_size)
            groups.append([self.active_players[i] for i in sample_idxs])
            for i in sample_idxs:
                unassign_idxs.remove(i)
            previous_idxs = sample_idxs

        if unassign_idxs:
            if len(unassign_idxs) > min_size:
                groups.append([self.active_players[i] for i in unassign_idxs])
            else:
                groups.pop()
                sample_idxs = sample(unassign_idxs.union(previous_idxs), max_size - 1)
                groups.append([self.active_players[i] for i in sample_idxs])
                groups.append([self.active_players[i] for i in unassign_idxs])
        print("assigned groups of", [len(group) for group in groups])
        return groups

    def run_games(self, player_groups, game_config):
        """Runs the one round of games for players assigned to each of the groups, winners from each group becomes active players again in the next rounds of games, empties out active player at the start of the games and fills it back in as winners from each group are determined.

        Args:
            player_groups ([list(list(IPlayer))): a list of lists of players
            game_config (dict): a dict of game configurations to give the referee for the specific game construction
        """
        self.active_players.clear()

        for group in player_groups:
            print("starting game for players", [player.get_id() for player in group])
            winners, kicked = Referee(game_config, group, observers=self.observers).run_game()

            self.kicked_players.extend(kicked)

            self.active_players.extend(winners)

            self.losers.extend([player for player in group if (player not in winners) and (player not in kicked)])

    def inform_all(self, event, info):
        """Informs all the players and observers of a tournament event with the given info to pass along.

        Args:
            event (int): a integer event code
            info (list): a list of argument information
        """
        for player in self.active_players:
            safe_execution(self.get_inform_executor(player, event), info)

        for observer in self.observers:
            safe_execution(self.get_inform_executor(observer, event), info)

    def get_inform_executor(self, informee, event):
        """Gets the executor for the given informee of the specified event.

        Args:
            informee (IObserver): a observer of the tournament, player included
            event (int): a integer event code

        Returns:
            func: an executor function
        """
        executor_table = {
            self.TOURNAMENT_START: informee.tournament_start_update,
            self.TOURNAMENT_PROGRESS: informee.tournament_progress_update,
            self.TOURNAMENT_END: informee.tournament_end_update
        }
        return executor_table[event]