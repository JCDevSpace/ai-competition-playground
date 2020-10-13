
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
    # players is a List[Player]
    # board is a Board
    def __init__(self, players, board):
        self.players = sorted(players, keys=(lambda x : x.get_age()))
        self.board = board
        self.penguin_positions = {}
        self.turn = 0
        # self.scores = {}

        for player in self.player
            self.penguin_positions[player] = {}
            # self.scores[player] = 0

    def get_current_player(self):
        return self.players[self.turn]

    def place_penguin(self, player, posn):
        if self.board.is_open(posn):
            # TODO: possibly implenting score here
            # fish = self.board.get_tile()
            # self.scores[player] += fish
            self.board.set_tile(0, posn)
            self.penguin_positions[player].append(posn)
        else:
            raise ValueError("placing penguin on invalid tile")

    def move_penguin(self, player, start_posn, end_posn):
        if start_posn in self.penguin_positions[player] and end_posn in self.board.get_valid_moves(start_posn):
            self.place_penguin(player, end_posn)
            self.penguin_positions[player].remove(start_posn)
            self.penguin_positions[player].add(end_posn)
        else:
            raise ValueError("invalid move")

    def game_over(self):
        for player in self.players:
            if self.has_moves_left(player):
                return False
        return True

    def has_moves_left(self, player):
        for posn in self.penguin_positions[player]:
            if len(self.board.get_valid_moves(posn)) > 0:
                return True
        return False

    def get_game_state(self):
        player_data = [ player.get_data() for player in self.players ]
        penguin_positions = { player.get_color(): positions for player, positions in self.player_positions.items() }

        return (self.board.get_board_state(), player_data, penguin_positions, self.turn)
