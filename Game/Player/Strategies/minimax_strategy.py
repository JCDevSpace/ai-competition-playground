from Game.Player.i_strategy import IStrategy


class MinimaxStrategy(IStrategy):
    """
    A MinimaxStrategy represents a strategy that uses the minimax algorithm to find the best action in a game tree looking a certain depth ahead.

    This class implements the IStrategy interface.
    """

    def __init__(self, eval_func, depth=2):
        """Initializes a minimax strategy.

        Args:
            eval_func (func(IState)): a function that takes a game state and evaluates it to a non negative integer value.
            depth (int, optional): a positive integer of how many levels down the search tree to look ahead when performing the minimax search. Defaults to 2.
        """
        self.eval_func = eval_func
        self.depth = depth

    def get_action(self, game_state):
        """Gets the move that maximizes the current player's score by looking ahead using a search tree of future states. The underlaying strategy assumes the opposing players minimize the calling player's score, returns false if the given state is already in the game over state.

        Args:
            game_state (game_state): a game state to find best action for

        Returns:
            union(Action, false): an action to take base on the minimax finding or false
        """
        if not game_state.game_over():
            max_agent = game_state.current_player
            return max(game_state.valid_actions(), \
                        key=lambda action: self.state_value(game_state.successor_state(action), 0, max_agent))
        return False

    def state_value(self, state, depth, max_agent):
        """Finds the values of the given state looking a certain depth ahead and the specified max agent using the minimax algorithm, the value of the state is derived from the yield of the eval function.

        Args:
            state (IState): a game state to evalute a value for
            depth (int): a non negative integer representing the remaining depth to search in the tree of game states
            max_agent (str): a color str representing the player to miximize the value for

        Returns:
            int: a non negative value derived from the yield of the evaluation function
        """

    
