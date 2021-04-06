class IObserver:
    """
    An IObserver is the observer interface of the board game tournaments, ensuring functionality to process updates in the progress of individual games and the tournament as a whole.
    """

    async def game_start_update(self, game_state):
        """Updates the observer on the start of a board game by consuming the given starting players and the game state.

        Args:
            game_state (IState): a game state object
        """
        pass

    async def game_action_update(self, action, game_state):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
            game_state (IState): a game state object
        """
        pass

    async def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        pass
    
    async def tournament_start_update(self, players):
        """Updatest the observer on the start of a board game tournament with the initial contestents.

        Args:
            players (list(str)): a list of string representing player names
        """
        pass

    async def tournament_progress_update(self, match_ups):
        """Updates the observer on the progress of a board game tournament by consuming the given players who advanced to the next round and the players who got knocked out.

        Args:
            match_ups (list): a lisg of list of player names where each list is the group of players in a match.
        """
        pass

    async def tournament_end_update(self, winners):
        """Updates the observer on the final winners of the board game tournament. 

        Args:
            winners (list(str)): a list of player names
        """
        pass