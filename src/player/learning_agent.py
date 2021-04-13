from src.player.i_player import IPlayer

from src.common.util import flip_coin, chose_randomly
from copy import deepcopy


class LearningAgent(IPlayer):

    def __init__(self, name, unique_id, training_episodes=3000, epsilon=0.5, alpha=0.5, gamma=1):
        """Initializes a AI player that uses a specific tree search strategy to find the best action in a board game.

        Args:
            name (str): a alphanumeric player name, less than 12 chars
            unique_id (int): a non negative integer uniquely identifies a player in the system
            training_episodes (int): a non negative integer to specified how many episodes the learning agent will observe and learn, no more learning (updates to qvalues) after reaching the required number of training episodes.
        """
        self.name = name
        self.id = unique_id
        self.training_episodes = training_episodes

        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = gamma

        self.state = None
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = None

        self.qvalues = {}
        self.default_qvalue = 0

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    async def game_start_update(self, game_state):
        """Updates the observer on the start of a board game by consuming the given starting players and the game state.

        Args:
            game_state (IState): a game state object
        """
        self.state = game_state

    async def game_action_update(self, action, game_state):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
            game_state (IState): a game state object
        """
        if self.state:
            self.state.apply_action(action)
        else:
            self.state = game_state

    async def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        if player != self.color and self.state:
            self.state.remove_player(player)

    async def playing_as(self, color):
        """Updates the player the color that it's playing as in a board game.

        Args:
            color (str): a color string
        """
        self.color = color

    async def get_action(self, game_state):
        """Finds the action to take in a board game by consuming the given game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args:
            game_state (IState): a game state object

        Returns:
            Action: an action to take
        """
        action = False
        if self.training_episodes:
            self.training_episodes -= 1
            await self.observation_update()
            if flip_coin(1 - self.epsilon):
                action = await self.max_qvalue_action()
            else:
                action = chose_randomly(self.state.valid_actions())
            self.prev_state = deepcopy(self.state)
            dummy_state = deepcopy(self.state)
            _, reward = dummy_state.apply_action(action)
            self.prev_action = action
            self.prev_reward = reward
        else:
            action = await self.max_qvalue_action()
        return action

    async def max_qvalue_action(self):
        best_value = float('-inf')
        best_action = False
        for action in self.state.valid_actions():
            qvalue = self.qvalues.get((self.state, action), self.default_qvalue)
            if qvalue > best_value:
                best_value = qvalue
                best_action = action
        return best_action

    async def observation_update(self):
        print("Training episode remaining", self.training_episodes)
        best_value = float('-inf')
        if not self.state.game_over():
            for action in self.state.valid_actions():
                qvalue = self.qvalues.get((self.state, action), self.default_qvalue)
                if qvalue > best_value:
                    best_value = qvalue
            sample = 1 + self.discount * best_value
        else:
            sample = 100 if self.color in self.state.game_winners() else 0

        self.qvalues[(self.prev_state, self.prev_action)] = (1 - self.alpha) * self.qvalues.get((self.state, action), self.default_qvalue) + self.alpha * sample
        
