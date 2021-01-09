class IStrategy:
    """
    An IStrategy is the interface for a player strategy when playing a board game, providing funtionality to find the best actions in a board game based on the implemented strategy to have the best chance at winning.
    """

    def get_action(self, game_state):
        """Finds the best action based on the implemented strategy for the given game state, returns false if the given state is already in the game over state.

        Args:
            game_state: The game state to find the best action for

        Returns:
            union(Action, false): An action to take in a board game or false
        """
        pass