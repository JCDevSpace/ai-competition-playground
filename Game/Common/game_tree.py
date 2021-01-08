from copy import deepcopy


class GameTree:
    """
    A GameTree is a union of:
    -GameState:
        the state of a game in the current tree node, root of the current tree
    -Dict{Action : GameTree})
        a children dictionary with valid actions from the current node game state as keys and children nodes with the new game state of the node as the one after applying the action from the state in the current node   

    A GameTree represents a tree of game state nodes and their children, where each node contains a state and action as edge connections to child nodes that have a new state as the result of applying the corresponding actions.

    If a node has no child, it mean tha game is over at that state.
    """

    
    def __init__(self, state):
        """Creates a GameTree given an initial state. The children are not yet generated on initialization to save space and will be generated on demand automatically when it's needed.

        Args:
            state (GameState): the game state corresponding with the current node
        """
        self.state = state
        self.children = {}

    def generate_children(self):
        """Generates all the children nodes and stores it in the children dictionary for easy retrieval, does nothing if the children is already generated for this node.
        """
        if not self.children:
            for action in self.state.valid_actions():
                node = self.resulting_node(action)
                if node:
                    self.children[action] = node

    def resulting_node(self, action):
        """Generates the new child node as a result of applying the given action from the state of the current node.

        Args:
            action (Action): an action

        Returns:
            union(GameTree, false): a new GameTree node or false if the action can't be successfully applied to the state of the current node.
        """
        state = deepcopy(self.state)

        if state.apply_action(action):
            return GameTree(state)
        return False

    def apply(self, function):
        """Generates a dictionary of each valid action to the the yield of the function of the it's children trees.

        Args:
            function (func(GameTree)): a function object that can perform some operation on a game tree node and returns some result

        Returns:
            dict(action:func(GameTree)): a dictionary of action and the result of the function applied on the node from applying the action to the state of the current node
        """
        results = {}

        if not self.children:
            self.generate_children()
        
        for action, tree in self.children.items():
            results[action] = function(tree)

        return results

    def get_node_state(self):
        return deepcopy(self.state)

    def get_children(self):
        if not self.children:
            self.generate_children()
        return self.children
