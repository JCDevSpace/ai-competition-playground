import copy

from Game.Common.i_board import IBoard, BoardType
from Game.Common.action import action_type


class CheckerBoard(IBoard):
    """
    A CheckerBoard is a combination of:
    - list(list(int)):
        2D list representing the 2D board layout with each cell containing either 0, 1 or 2, where a 0 represents an empty spot, 1 represents
        the a man piece at the spot and 2 represents a king piece at the spot.

    - dict(str:list(Posn)):
        a dictionary of color string white and red representing a player and their corresponding avatar positions on the board.

    A CheckerBoard represents a squre grid of tiles for the game of checker(English board and rules) with layoutof the indices as specified below:

    ╔═══════╤═══════╤═══════╗
    ║ (0,0) │ (0,1) │ (0,2) ║
    ╠═══════╪═══════╪═══════╣
    ║ (1,0) │ (1,1) │ (1,2) ║
    ╟───────┼───────┼───────╢
    ║ (2,0) │ (2,1) │ (2,2) ║
    ╚═══════╧═══════╧═══════╝

    A CheckerBoard implements the IBoard interface.
    """

    EMPTY = 0
    MAN = 1
    KING = 2

    def __init__(self):
        """Initilizes a standard 8x8 English Checker board with both player avatars placed in their default positions.
        """
        self.size = 8
        self.avatars, self.layout = self.generate_default_board()

    def generate_default_board(self):
        """Generates the default avatar placements and board layout. 

        Returns:
            tuple(dict, list(list): a tuple where the first is the dictionary of player color to it's corresponding avatar placements and the second a 2D list of the board list
        """
        avatars = {"white":[],"red":[]}
        layout = []

        for r in range(self.size):
            layout.append([])
            for c in range(self.size):
                spot = self.EMPTY
                if self.legal_posn((r,c)):
                    if self.white_starting_rows(r):
                        avatars["white"].append((r,c))
                        spot = self.MAN
                    elif self.red_starting_rows(r):
                        avatars["red"].append((r,c))
                        spot = self.MAN
                layout[r].append(spot)

        return avatars, layout

    def legal_posn(self, posn):
        """Determines if the given position is a legal postion for an avatar.

        Args:
            posn (Posn): a position

        Returns:
            bool: a boolean with true indicating it's legal
        """
        return (posn[0] % 2) != (posn[1] % 2)

    def white_starting_rows(self, r):
        return r <= 2

    def red_starting_rows(self, r):
        return r >= 5

    def set_custom_board(self, avatars, layout):
        """Sets a custom board with the given avatar positions and layout.

        Args:
            avatars (dict): a dictionary of players and their corresponding avatar list
            layout (list(list)): a 2D list of the board layout
        """
        self.avatars = copy.deepcopy(avatars)
        self.layout = copy.deepcopy(layout)

    def set_layout(self, layout):
        """Sets the layout of the board to the given one.

        Args:
            layout (2d list): 2d list of the board grid layout

        Returns:
            bool: a boolean with true indicating layout set successfully
        """
        try:
            if len(layout) == 2:
                self.layout = copy.deepcopy(layout)
                print("Layout set properly")
                return True
        except Exception as e:
            print(e)
        return False

    def set_avatars(self, avatars):
        """Sets the avatars of the board to the given one.

        Args:
            avatars (dict): a dictionary with player color as keys and corresponding lists of Posn as the positions of avatars they have

        Returns:
            bool: a boolean with true indicating avatars set successfully
        """
        try:
            if len(self.avatars) == len(avatars):
                self.avatars = copy.deepcopy(avatars)
                print("Avatars set properly")
                return True
        except Exception as e:
            print(e)
        return False

    def valid_actions(self, player):
        """Finds the list of valid actions for the given player on the checker board, returns empty list if there are no valid actions for the specified player including the player doesn't exist on the board.

        Args:
            player (str): a color string representing a player

        Returns:
            list(Action): a list of actions that can be performed
        """
        actions = []

        if player in self.avatars:
            self.has_jump = self.have_jumps(player)
            actions = [(from_posn, to_posn) for from_posn in self.avatars[player] for to_posn in self.reachable_positions(player, from_posn)]

        return actions

    def have_jumps(self, player):
        """Determin if the given player has any jump moves.

        Args:
            player (str): a color string representing the player

        Returns:
            bool: a boolean with true indicating having jumps
        """
        opponent = "white" if player == "red" else "red"

        for from_posn in self.avatars[player]:
            moveset_deltas = self.get_moveset_deltas(player, from_posn)
            for deltas in moveset_deltas:
                if self.can_jump(opponent, from_posn, deltas):
                    # print(player, "have jumps")
                    return True
        return False

    def can_jump(self, opponent, from_posn, deltas):
        """Determines whether with the given starting position, opponent player, and move deltas there exist a valid jump, if so returns the to position for the jump else returns False, a jump is possible if there is a piece from the opponent in an diagonal adjacent spot and the diagonal adjacent spot after that is empty.

        Args:
            opponent (str): a color string representing a player
            from_posn (Posn): a position
            deltas (tuple): a tuple with first representing row and second the column delta in a move calculation 

        Returns:
            Union(False, Posn): a boolean or a position
        """
        stepping_stone = (from_posn[0] + deltas[0], from_posn[1] + deltas[1])
        if self.in_bound(stepping_stone) \
                and stepping_stone in self.avatars[opponent]:
            to_posn = (stepping_stone[0] + deltas[0], stepping_stone[1] + deltas[1])
            if self.in_bound(to_posn) and self.is_empty(to_posn):
                return to_posn
        return False

    def reachable_positions(self, player, from_posn):
        """Finds the list of reachable positions for the player from the given starting position, a postions is reachable for a given player and starting position if there are possible jumps or if there are no jumps, there is a diagonal position adjacent, regular moves are not consider reachable if the player have any available jumps.

        Args:
            player (str): a color string representing a player
            from_posn (Posn): a position to start from

        Returns:
            list(Posn): a list of positions reachable
        """
        moveset_deltas = self.get_moveset_deltas(player, from_posn)
        
        if self.has_jump:
            opponent = "white" if player == "red" else "red"
            return self.get_diagonal_jumps(opponent, from_posn, moveset_deltas)
        else:
            return self.get_diagonal_moves(from_posn, moveset_deltas)

    def get_diagonal_jumps(self, opponent, from_posn, moveset_deltas):
        """Finds all valid diagonal jumps in each of the 4 direction, returns empty list if there are no possible jumps.

        Args:
            opponent (str): a color string representing a player
            from_posn (Posn): a position to start from

        Returns:
            list(Posn): a list of positions
        """
        jumps = []

        for deltas in moveset_deltas:
            to_posn = self.can_jump(opponent, from_posn, deltas)
            if to_posn:
                jumps.append(to_posn)

        return jumps

    def get_diagonal_moves(self, from_posn, moveset_deltas):
        """Finds all valid diagonal moves in each of the 4 direction, returns empty list if there are no possible moves.

        Args:
            from_posn (Posn): a postion to start from
            moveset_deltas (list): a list of row and column deltas

        Returns:
            list(Posn): a list of postion
        """
        moves = []

        for delta_r, delta_c in moveset_deltas:
            to_posn = (from_posn[0] + delta_r, from_posn[1] + delta_c)
            if self.in_bound(to_posn) and self.is_empty(to_posn):
                moves.append(to_posn)
        
        return moves

    def is_empty(self, posn):
        return self.layout[posn[0]][posn[1]] == self.EMPTY

    def in_bound(self, posn):
        return posn[0] >= 0 and posn[0] < self.size \
                    and posn[1] >= 0 and posn[1] < self.size

    def get_moveset_deltas(self, player, from_posn):
        """Finds the list of moveset deltas in row and column for the given player and starting position.

        Args:
            player (str): a color string representing a place
            from_poosn (Posn): a position of the piece
        Returns:
            list(tuple): a list of tuples with the first as the row and second the column delta
        """
        if self.layout[from_posn[0]][from_posn[1]] == 2:
            return [(-1,-1), (-1, 1), (1, -1), (1, 1)]
        elif player == "white":
            return [(1, -1), (1, 1)]
        else:
            return [(-1, -1), (-1, 1)]

    def apply_action(self, player, action):
        """Applies the given action for the player on the current game board and returns a reward if there is any.

        Args:
            action (Action): an action to apply

        Returns:
            tuple(bool, int): a tuple with the first a boolean indicating whether the action was successful and the second a reward if the action was successfuly.
        """
        success = False
        reward = 0

        if action_type(action).is_valid() \
                and action in self.valid_actions(player):

                self.update_player_avatars(player, *action)
                self.update_player_layout(*action)

                if self.is_jump(*action):
                    opponent = "white" if player == "red" else "red"
                    self.update_opponent(opponent, action)
                    reward = 1
                
                success = True
        
        return success, reward

    def update_player_avatars(self, player, from_posn, to_posn):
        """Updates the avatar list for the given player of the move with the given to and from positions.

        Args:
            player (str): a color string
            from_posn (Posn): a position
            to_posn (Posn): a position
        """
        avatar_idx = self.avatars[player].index(from_posn)
        self.avatars[player].pop(avatar_idx)
        self.avatars[player].insert(avatar_idx, to_posn)

    def update_player_layout(self, from_posn, to_posn):
        """Updates the layout for the move with the given to and from positions.

        Args:
            from_posn (Posn): a from position to update
            to_posn (Posn): a to position to move update
        """
        if self.layout[from_posn[0]][from_posn[1]] == self.MAN \
                and self.king_rows(to_posn[0]):
                self.layout[to_posn[0]][to_posn[1]] = self.KING
        else:
            self.layout[to_posn[0]][to_posn[1]] = self.layout[from_posn[0]][from_posn[1]]

        self.layout[from_posn[0]][from_posn[1]] = self.EMPTY

    def update_opponent(self, opponent, action):
        """Updates the layout and avatars of the given opponent in case of a jump action, requires the action to be a jump on the checker board.

        Args:
            opponent (str): a color string representing the oppent player to update
            action (Action): a jump action to update the oppoent with
        """
        stepping_r, stepping_c = self.stepping_stone(*action)
        self.layout[stepping_r][stepping_c] = self.EMPTY
        self.avatars[opponent].remove((stepping_r, stepping_c))

    def king_rows(self, r):
        """Determines if this is the row that man pieces will turn into kings.

        Args:
            r (int): a non negative integer representing a board row

        Returns:
            bool: a boolean with true indicating the man will turn into a king after reaching this row
        """
        return r == 0 or r == (self.size - 1)

    def is_jump(self, from_posn, to_posn):
        return (abs(to_posn[0] - from_posn[0]) > 1) \
                    or (abs(to_posn[1] - from_posn[1]) > 1)

    def stepping_stone(self, from_posn, to_posn):
        """Finds the position between the from and to posn used as the stepping stone for the jump.

        Args:
            from_posn (Posn): a position
            to_posn (Posn): a position

        Returns:
            Posn: a position of the stepping stone
        """
        r = from_posn[0]
        c = from_posn[1]

        delta_r = to_posn[0] - from_posn[0]
        delta_c = to_posn[1] - from_posn[1]
        
        if delta_r > 0:
            r += 1
        else:
            r -= 1

        if delta_c > 0:
            c += 1
        else:
            c -= 1

        return r, c

    def remove_player(self, player):
        """Removes the given player from game board.

        Args:
            player (str): a color string representing a player

        Returns:
            bool: a boolean with true indicating the player was successfully removed
        """
        if player in self.avatars:
            del self.avatars[player]
            return True
        return False

    def game_over(self):
        """Determines if the game is over with the board state.

        Returns:
            bool: a boolean with true indicating the game is over
        """
        if len(self.avatars) == 2:
            for player in self.avatars.keys():
                if not self.valid_actions(player):
                    return True
            return False
        return True

    def serialize(self):
        """Serializes information about the current game board to a dict of attritube with corresponding values.

        Returns:
            dict(X): a dictionary of attributes in the format specified as below:
            {   
                "board-type": BoardType.value,
                "info": {
                    "layout: list(list(int)),
                    "avatars": dict(str:list(Posn))
                }
            }
        """
        return {
            "board-type": BoardType.CHECKER.value,
            "info": {
                "layout": copy.deepcopy(self.layout),
                "avatars": copy.deepcopy(self.avatars),
            }
        }