from Common.View.Artist import Artist

# A Style is a Map(String, (Int or String)) which maps different stylistic constants to their values.

# A ScoreBoardArtist is responsible for rendering the scores of each player to the
# right of the Board rendering. It also shows which players turn it is.
class ScoreBoardArtist(Artist):

    # Generates a ScoreBoardArtist given the offsets and what type of tile to draw
    # Int, Int, List[Player], {Player: Int}, Int, Style -> ScoreBoardArtist
    def __init__(self, x_offset, height, player_data, score_data, turn, style):
        super().__init__(style)
        self.x_offset = x_offset
        self.height = height
        self.player_data = player_data
        self.score_data = score_data
        self.turn = turn

    # Draws the background of the scoreboard
    # Canvas -> Void
    def draw_background(self, canvas):
        canvas.create_rectangle(self.x_offset, 0,
            self.x_offset + self.style["scoreboard_width"],
            self.height, outline=self.style["scoreboard_outline"],
            fill=self.style["scoreboard_fill"],
            width=self.style["outline_width"])

    # Draws a scores of each player and indicates if it is their turn.
    # Canvas -> Void
    def draw_scores(self, canvas):
        start_x = self.x_offset + self.style["text_offset"]
        start_y = self.style["text_offset"]

        for index, player in enumerate(self.player_data):
            line_height = start_y + (index * (self.style["font_size"] + self.style["line_spacing"]))
            player_score = f"{player}: {self.score_data[player]}"

            if index == self.turn:
                player_score += " *"

            canvas.create_text(start_x, line_height, text = player_score)

    # Draws a scoreboard on a given canvas
    # Canvas -> Void
    def draw(self, canvas):
        self.draw_background(canvas)
        self.draw_scores(canvas)
