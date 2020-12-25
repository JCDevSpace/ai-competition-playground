
# An interface for a TournamentManager object
# The tournament manager is responsible for signing players
# up for tournaments and running tournamnets those players are in
class ManagerInterface():

    # starts the main loop of the manager
    # the main loop waits for players to sign up and
    # starts tournamnet in a seperate thread once enough players 
    # have signed up
    def start():
        pass

    # adds a player to the queue, so that the player
    # can wait until there are enough players to start a tournament
    def queue_player(self, player):
        pass

    # adds an observer to a local list of observers
    # when a tounament starts, these observers are passed
    # to the referee so that they can observe the game
    def add_observer(self, observer):
        pass

    # removes the number of players required for a tournament 
    # from the queue, then constructs a bracket and calls run_game
    # on each node of the tree that represents a game.
    # It returns the players who have won the tournament along with
    # the stats for each game returned by run_game
    def run_tournament(self, players):
        pass

    # Runs a game of fish by creating a new Referee and starting the game
    # Returns an 3 arrays of players: the winners, the losers, and the cheaters
    def run_game(self, players):
        pass