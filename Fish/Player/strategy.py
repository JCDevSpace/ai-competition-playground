class Strategy:

    def place_pengiun(self, game_state):
        board, _, penguin_positions, _, _ = game_state.get_game_state()
        all_penguins = set()
        for player, penguins in penguin_positions.items():
            all_penguins.update(penguins)
        num_rows = len(board)
        num_cols = len(board[0])
        for col in range(num_cols):
            for row in range(num_rows):
                if (row, col) not in all_penguins:
                    return row, col

        raise ValueError("No open spaces to place a penguin on")

    # Gets the best move to make looking N moves ahead.
    # N must be >= 1
    # GameTree, Natural -> Move
    def get_move(self, gametree, N):
        calling_player = gametree.get_current_player()
        move_scores = gametree.apply(lambda tree: self.minimax(tree, calling_player, N-1))
        max_val = max(move_scores.values())
        moves = [key for key, value in move_scores.items() if value == max_val]
        chosen = min(moves)
        return move_scores[chosen]

    # Returns the minimal maximum score after N turns for the calling player.
    # This assumes the opposing players minimize the calling player's score.
    # GameTree, Player, Natural -> Float
    def minimax(self, gametree, calling_player, N):
        current_player = gametree.get_current_player()

        if not gametree.get_children():
            if gametree.get_winners() == [calling_player]:
                return float('inf')
            elif calling_player in gametree.get_winners():
                return 0
            else:
                return -float('inf')

        else:
            if N <= 0:
                _, _, _, _, scores = gametree.get_current_state().get_game_state()
                return scores[calling_player.get_color()]

            if current_player == calling_player:
                move_scores = gametree.apply(lambda tree: self.minimax(tree, calling_player, N - 1))
                max_val = max(move_scores.values())
                moves = [key for key, value in move_scores.items() if value == max_val]
            else:
                move_scores = gametree.apply(lambda tree: self.minimax(tree, calling_player, N))
                min_val = min(move_scores.values())
                moves = [key for key, value in move_scores.items() if value == min_val]

            chosen = min(moves)
            return move_scores[chosen]



