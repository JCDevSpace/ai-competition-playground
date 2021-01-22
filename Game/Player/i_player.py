from Game.Common.i_observer import IObserver


class IPlayer(IObserver):
    """
    An IPlayer is an interface that extends the IObserver interface, ensuring additional functionality to process color assignment as well as request for actions in a game.
    """

    async def get_id(self):
        """Returns the player unique id.

        Returns:
            int: a non negative integer that uniquely identifies the player
        """
        pass

    async def get_name(self):
        """Returns the name of the player.

        Returns:
            str: a alphanumeric str with length less than 12 chars
        """
        pass

    async def playing_as(self, color):
        """Updates the player the color that it's playing as in a board game.

        Args:
            color (str): a color string
        """
        pass

    async def get_action(self, game_state):
        """Finds the action to take in a board game by consuming the given game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args:
            game_state (IState): a game state object

        Returns:
            Action: an action to take
        """
        pass