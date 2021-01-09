from Game.Common.i_observer import IObserver


class Player(IObserver):
    """
    An IPlayer is an interface that extends the IObserver interface, ensuring additional functionality to process color assignment as well as request for actions in a game.
    """

    def playing_as(self, color):
        """Updates the player the color that it's playing as in a board game.

        Args:
            color (str): a color string
        """
        pass

    def playing_with(self, colors):
        """Updates the player the other colors that it's playing against.

        Args:
            colors (list(str)): a list of color string
        """
        pass

    def get_action(self, game_state):
        """Finds the action to take in a board game given the current game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args

        Returns:
            Action: an action to take
        """
        pass