# A Move is one of
#   - (Player, Position, Position)
#   - (Player, False)
# the first of these represents a player moving their penguin from the first position to the second position
# The second of these represents when a player has no valid moves and passes their turn.

# A GameTree is a (GameState, Map{Move : GameTree})
# Where the GameState represents the current state of the game, and the map of moves to GameTree(s) represent
# the resulting GameTrees when that Move is taken.
class GameTree:

    # Creates a GameTree given an initial state. The children are not yet generated in order to save space,
    # to generate the children call GameTree.generate_children()
    def __init__(self, state):
        self.state = state
        self.children = None

    # Fills in the children mapping with populated GameTrees,
    # note: the children in this map will not have their children populated.
    # modifies self.children
    # Void -> Void
    def generate_children(self):
        self.children = {}
        for move in self.state.get_current_player_valid_moves():
            resulting = self.resulting_state(move)
            if resulting:
                self.children[move] = resulting

    # Returns the state which would result from doing the given Move on the initial state
    # Move -> Union(False, GameTree)
    def resulting_state(self, move):
        state = self.state.deepcopy()

        try:
            state.apply_move(move)
        except ValueError:
            return False

        return GameTree(state)


    # Returns the state corresponding to this part of the GameTree.
    # Void -> GameState
    def get_current_state(self):
        return self.state.deepcopy()

    # Applies the given function to all of the possible children and returns the map of each valid move
    # to the the yield of the function of the GameTree resulting from that move
    # (Func[GameTree] -> X) -> {Move : X}
    def apply(self, function):
        if self.children is None:
            self.generate_children()
        results = {}
        for move, resulting_tree in self.children.items():
            results[move] = function(resulting_tree)

        return results

    # Returns the children accessible from this GameTree
    # Void -> Map{Move, GameTree}
    def get_children(self):
        if self.children is None:
            self.generate_children()
        return self.children
