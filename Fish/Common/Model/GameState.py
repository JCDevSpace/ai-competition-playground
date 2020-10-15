
# A GameState is a (Board, List[Player], {Player, Set[Position]}, Int)
# The GameState object represents all the data need to run the fish game.
# The Board keeps track of the tiles and number of fish on those tiles,
# the List[Player] keeps information about the players in the game_state,
# and the {Player, List[Position]} keeps track of where the players penguins
# are on the board. The Int represents the index of the player whose turn it is.

# A Position is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

class GameState:


    # Creates a GameState given the Players playing and a Board
    # List[Player], Board -> GameState
    def __init__(self, players, board):
        self.players = sorted(players, key=(lambda x : x.get_age()))
        self.board = board
        self.penguin_positions = {}
        self.turn = 0
        # self.scores = {}

        for player in self.players:
            self.penguin_positions[player] = {}
            # self.scores[player] = 0

    # Returns the player who's turn it is currently
    # Void -> Player
    def get_current_player(self):
        return self.players[self.turn]

    # Adds a penguin for a particular player at a Position
    # Modifies self.board, and self.penguin_positions
    # Player, Position -> Void
    # raises ValueError if trying to place a penguin at a non-open Position (has penguin there already or is a hole)
    def place_penguin(self, player, posn):
        if self.board.is_open(posn):
            # TODO: possibly implenting score here
            # fish = self.board.get_tile()
            # self.scores[player] += fish
            self.board.set_tile(0, posn)
            self.penguin_positions[player].append(posn)
        else:
            raise ValueError("placing penguin on invalid tile")

    # Attempts to Move a player's penguin from the start Position to the End Position
    # Modifies self.board and self.penguin_positions
    # Player, Position, Position -> Void
    # raises ValueError if there is no penguin for that player at the start Position or if the end position is not a valid move from the start Position
    def move_penguin(self, player, start_posn, end_posn):
        if start_posn in self.penguin_positions[player] and end_posn in self.board.get_valid_moves(start_posn):
            self.place_penguin(player, end_posn)
            self.penguin_positions[player].remove(start_posn)
            self.penguin_positions[player].add(end_posn)
        else:
            raise ValueError("invalid move")

    #Returns whether or not the game is over, meaning no one can move.
    # Void -> Boolean
    def game_over(self):
        for player in self.players:
            if self.has_moves_left(player):
                return False
        return True

    #Returns whether or not a specific player has any available moves
    # Player -> Boolean
    def has_moves_left(self, player):
        for posn in self.penguin_positions[player]:
            if len(self.board.get_valid_moves(posn)) > 0:
                return True
        return False

    # Returns the GameState as defined at the top of the file.
    # Void -> GameState
    def get_game_state(self):
        player_data = [ player.get_data() for player in self.players ]
        penguin_positions = { player.get_color(): positions for player, positions in self.penguin_positions.items() }

        return (self.board.get_board_state(), player_data, penguin_positions, self.turn)
