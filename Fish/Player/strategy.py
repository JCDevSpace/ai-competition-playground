
# Static class for players to use for making decisions about their moves.
class Strategy:

    # Returns the placement the player should make at the beginning of
    # the game by first filling up the first row from left to right
    # and moving on to subsequent rows
    # GameState -> Position
    # raises ValueError if unable to find a position to place the penguin
    def get_placement(game_state):
        board, _, penguin_positions, _, _ = game_state.get_game_state()
        all_penguins = set()
        for player, penguins in penguin_positions.items():
            all_penguins.update(penguins)

        num_rows = len(board)
        num_cols = len(board[0])
        for row in range(num_rows):
            for col in range(num_cols):
                if (row, col) not in all_penguins and board[row][col] != 0:
                    return row, col

        raise ValueError("No open spaces to place a penguin on")

    # Gets the move that maximizes the current player's score
    # by looking ahead to states where the current player makes N moves.
    # This assumes the opposing players minimize the calling player's score.
    # N must be >= 1
    # GameTree, Natural -> Move
    def get_move(gametree, N):
        calling_player = gametree.get_current_state().get_current_color()

        # find the minimax value of possible moves
        move_scores = gametree.apply(lambda tree: Strategy.minimax(tree, calling_player, N-1))

        # if game is over throw an error, there are nno moves that can be made
        if not move_scores:
            raise ValueError("the game is over")

        # return the move with the highest minimax value
        max_val = max(move_scores.values())
        moves = [key for key, value in move_scores.items() if value == max_val]
        return Strategy.tiebreaker(moves)

    # Returns the minimal maximum score after N turns for the calling player.
    # This assumes the opposing players minimize the calling player's score.
    # GameTree, Player, Natural -> Float
    def minimax(gametree, calling_player, N):
        current_player = gametree.get_current_state().get_current_color()

        # if the tree depth or a leaf node has been reached return the score of
        # the calling player
        if not gametree.get_children() or N <= 0:
            _, _, _, _, scores = gametree.get_current_state().get_game_state()
            return scores[calling_player]

        # Otherwise recur on the possible moves of the player whose turn it is.
        # The calling maximizes the outcomes and the other players try to minimize it
        if current_player == calling_player:
            move_scores = gametree.apply(lambda tree: Strategy.minimax(tree, calling_player, N - 1))
            max_val = max(move_scores.values())
            moves = [key for key, value in move_scores.items() if value == max_val]
        else:
            move_scores = gametree.apply(lambda tree: Strategy.minimax(tree, calling_player, N))
            min_val = min(move_scores.values())
            moves = [key for key, value in move_scores.items() if value == min_val]


        chosen = Strategy.tiebreaker(moves)
        return move_scores[chosen]

    # Because of the way tuple comparison works in python,
    # calling min on our array of Moves exhibits the same
    # tie breaking behavior specified in the assignment where
    # first the move with the lowest starting position is chosen
    # and afterwards if it is still a tie the moves with the lowest
    # end position is chosen. A position is lower if the row of a
    # position is lower, and if the row is the the same then the one
    # with the lower column is lower.
    # List[Move] -c Move
    def tiebreaker(moves):
        return min(moves)
