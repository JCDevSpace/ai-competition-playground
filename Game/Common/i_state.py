class IState:
    """
    A IState is the interface for the state of board games, ensuring all proper implementations of the state provide the essential functionality to find all valid actions, applying a given action, find the current player, kick a player, determin if a game is over, finding the winners if it is and provide serialized copies of it's internal data representation. 
    """
    
    def valid_actions(self):
        """Finds the list of valid action from the current game state, returns false if there are no player in the current game state.

        Returns:
            union(list(Action), false): a list of actions or false if there are no players in the current game state.
        """
        pass


    def apply_action(self, player, action):
        """Applies the given action to the game state.

        Args:
            action (IAction): the game action to apply
        
        Returns:
            bool: a boolean with true representing the action is applied properly and the curent state advanced
        """
        pass

    def current_player(self):
        """Finds the player who's turn it is currently, returns false if there are no player in the curent game state.

        Returns:
            union(str, false): the color string representing the player or false meaning there are no players in the game
        """
        pass

    def game_over(self):
        """Check whether the game is over with the current game state.

        Returns:
            bool: a boolean with true representing that the game is over
        """
        pass

    def remove_player(self, player):
        """Removes the given player from the current game state.

        Args:
            player (str): the color string representing the player to kick

        Returns:
            bool: a boolean with true representing the player is removed properly
        """
        pass

    def game_score(self, player):
        """Finds the score of the given player in the current game,returns false if the player doesn't exist in the game.

        Args:
            player (str): the color string representing the player

        Returns:
            union(int, false): a non negative integer representing the score or false if palyer is not found
        """
        pass

    def serialized(self):
        """Serializes information that represents the current game state into a map of attribute with corresponding values.

        Returns:
            dict(x): a dictionary with important attributes as key-value pairs in the following format:
            {   
                "players": list(str),
                "scores": dict(str:int),
                "board": IBoard.serialize()
            }
        """
        pass