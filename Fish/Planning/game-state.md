# Game State

## Board
Tile is one of Number or Color
Where Color is one of "red", "black" ...

List[List[Tile]] tiles

Penguins: {Player: [(Int, Int), ...]} for each player the list of their Penguins represented by a pair of integers for their position on the board.

|-> get_board_state() void -> List[List[Int]]

|-> move(row_start, row_end, col_start, col_end): Int, Int, Int, Int -> void can Throw exception

|-> remove_penguins_belonging_to(Player)

|-> place_penguins(Player, (row, col))

## Tile
hold number of fish, and if its a hole

|-> __init__(num_fish, is_hole) Int, Boolean -> Void

|-> get_fish() void -> Int

|-> is_hole() void -> Boolean



## Referee

Contains a board, and way to validate rules, and players communicate with it to attempt moves

Board board,

Board View view,

List[Player] players


Player current_turn

4 allowed colors -- CONSTANT

|-> __init__(min_1_fish = None, num_holes = None)

|->  generate_board (min_1_fish = None, num_holes = None) -> Board

|-> kick_player(player)

|-> try_move(player, (start), (end))

|-> "private" validate_move(player, (start), (end))

|-> draw()


## Board View
Canvas to draw board on

talks to controller to get get board State

draws it based on list[list[int]]

|-> draw(List[List[int]])


## Player
Age

Color

implement __comp__ to sort by age

get_color() void -> (Int, Int, Int) rgb value
