class IState:
    """
    A IState is the interface for the state of board games, ensuring all proper implementations of the state provide the essential functionality to find all valid actions, applying a given action, find the current player, kick a player, determin if a game is over, finding the winners if it is and provide serialized copies of it's internal data representation. 
    """
    
    def valid_actions(self):
        """Finds the list of valid action from the current game state.

        Returns:
            List(IAction): a list of actions
        """
        pass


    def apply_action(self, player, action):
        """Applies the given action to the current game state for the given player.

        Args:
            player (str): a color string representing a player
            action (IAction): the game action to apply
        
        Returns:
            bool: a boolean with true representing the action is applied properly and the curent state advanced, and false for atemtping to apply an invalid action or not the current player's turn
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