from src.player.strategies.i_strategy import IStrategy
from random import randint


class PrunedMinimaxStrategy(IStrategy):
    """
    A PrunedMinimaxStrategy is a combination of:
    -func:
        a function that takes a game state and evaluates it to a non negative integer
    -int:
        a positive integer representing how many level to look ahead in the tree of game states.
        
    A PrunedMinimaxStrategy represents a strategy that uses the minimax algorithm and pruning paths with known less rewards to find the best action in a game tree looking a certain depth ahead, the pruning is aimed to reduce computation needed when searching but still achieve the same results as regular minimax.

    This class implements the IStrategy interface.
    """

    def __init__(self, eval_func, depth):
        """Initializes a minimax strategy.

        Args:
            eval_func (func(IState)): a function that takes a game state and evaluates it to a non negative integer value.
            depth (int): a positive integer of how many levels down the search tree to look ahead when performing the minimax search
        """
        self.eval_func = eval_func
        self.depth = depth

    def get_action(self, game_state):
        """Gets the move that maximizes the current player's score by looking ahead using a search tree of future states. The underlaying strategy assumes the opposing players minimize the calling player's score, and prunes any branches that will yield less then the currently known best reward, returns false if the given state is already in the game over state.
        
        Args:
            game_state (IState): a game state to find best action for

        Returns:
            union(Action, false): an action to take base on the minimax finding or false
        """
        if not game_state.game_over():
            alpha = float("-inf")
            beta = float("inf")
            self.max_agent = game_state.current_player()
            action_values = {action:self.state_value(game_state.successor_state(action), 0, alpha, beta) for action in game_state.valid_actions()}

            highest_val = max(action_values.values())

            best_actions = [action for action, value in action_values.items() if value == highest_val]

            if len(best_actions) == 1:
                return best_actions[0]
            else:
                return self.tie_break(best_actions)
        return False

    def state_value(self, state, depth, alpha, beta):
        """Finds the values of the given state looking a certain depth ahead for the max agent using the minimax algorithm, the value of the state is derived from the yield of the eval function.

        Args:
            state (IState): a game state to evalute a value for
            depth (int): a non negative integer representing the remaining depth to search in the tree of game states
            alpha (float): max agent's best option so far
            beta (float): min agent's best option so far

        Returns:
            int: a non negative value derived from the yield of the evaluation function
        """
        if state.game_over():
            return self.eval_func(self.max_agent, state)
        elif state.current_player() != self.max_agent:
            return self.min_value(state, depth, alpha, beta)
        else:
            return self.max_value(state, depth + 1, alpha, beta)

    def min_value(self, state, depth, alpha, beta):
        """Finds the minimum evaluation value for the given state.

        Args:
            state (IState): a game state
            depth (int): a non negative integer
            alpha (float): max agent's best option so far
            beta (float): min agent's best option so far

        Returns:
            int: a non negative integer
        """
        v = float('inf')
        for action in state.valid_actions():
            successor = state.successor_state(action)
            if successor.current_player() == self.max_agent \
                    and depth == self.depth - 1:
                v = min(v, self.eval_func(self.max_agent, successor))
            else:
                v = min(v, self.state_value(successor, depth, alpha, beta))
            
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, state, depth, alpha, beta):
        """Finds the maximum evaluation value for the given state.

        Args:
            state (IState): a game state
            depth (int): a non negative interger
            alpha (float): max agent's best option so far
            beta (float): min agent's best option so far

        Returns:
            int: a non negative integer
        """
        v = float('-inf')
        for action in state.valid_actions():
            v = max(v, self.state_value(state.successor_state(action), depth, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def tie_break(self, actions):
        """Picks an action from the given list of actions when there are multiple moves that provide the same value toward winning the game.

        Args:
            actions (list(Action)): a list of actions

        Returns:
            Action: an Action
        """
        return actions[randint(0, len(actions) - 1)]


    
