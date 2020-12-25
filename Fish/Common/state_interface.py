class IState:
    """
    A IState represents the state of a board game, handles keeping track of information of the different players and the board.
    """

    def apply_action(self, action):
        """Applies the given action to the current game state.

        Args:
            action (IAction): the game action to apply
        
        Returns:
            bool: a boolean with true representing the action is applied properly and the curent state advanced, and false for atemtping to apply an invalid action
        """
        pass

    def current_player(self):
        """Finds the player who's turn it is currently.

        Returns:
            str: the color string representing the player
        """
        pass

    def game_over(self):
        """Check whether the game is over with the current game state.

        Returns:
            bool: a boolean with true representing that the game is over and false not
        """
        pass

    def remove_player(self, player):
        """Removes the given player from the current game state.

        Args:
            player (str): the color string representing the player to kick

        Returns:
            bool: a boolean with true representing the player is removed properly and false not
        """
        pass

    def game_winners(self):
        """Finds the winner of the game if the game is over, required to check whether the game is over first.

        Returns:
            list(str): a list of strings with each element representing a winner's unique color string 
        """
        pass

    def serialized(self):
        """Serializes information that represents the current game state into a map of attribute with corresponding values.

        Returns:
            dict(x): a dictionary with important attributes as key-value pairs
        """
        pass

    def valid_actions(self):
        """Finds the list of valid action from the current game state.

        Returns:
            List(IAction): a list of game actions
        """
        pass
