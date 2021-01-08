

class Referee:
    """
    A Referee is a union of:
    -GameTree:
        a GameTree of the running board game
    -list(Player):
        a list of player objects to interact to run the game
    -list(Obsever):
        a list of observer objects to update game the game
    """

    def __init__(self, players, observer=None):
        self.players = players
        
        if observer:
            self.observer = observer
        else:
            self.observer = []

        self.game_tree = self.initialize_game_tree()


    def perform_action(self, action):
        return False

    def kick_player(self, player_color):
        return False

    def run_game(self):
        return False

    def action_update(self):
        return False

