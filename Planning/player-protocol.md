# Player Protocols
----
After connecting to the server, the clients will be able to query the player-interface
so that they can play the Fish game. The players will send these queries to the server
in a json format and get responses to the queries also in json format. We have not decided
the exact method of communication. But it will most likely be over TCP or HTTP.

The Game takes place in a series of 4 phases, which are the following:
- "waiting": before the game starts and the referee is wait for other people to join
- "placement": the setup portion of the game where players take turns placing their penguins
- "playing": this is the standard phase where players take turns to accumulate points
- "finished": once the game is over and a winner has been decided it moves to this GamePhase

When a player first connects to the server they are put into a lobby, while waiting for other
players to join. At this point the game has started and the players in the lobby can begin to make queries to the server. Once everyone has joined the game will begin to move through the game phases

When a player sends a query to the server it must be in the following format:

```
{
  query: "query_name",
  params: {
    param_name: param_value,
    .
    .
    .
  }
}

```

If players send queries in invalid formats then they will be kicked from the game. This means
their penguins are removed from the board and their connection is closed.

Other actions that can result in getting kicked include:
- Sending a query during the wrong phase of the game
- taking to long to make a move

-----
## Possible queries:
```
query_name: "get_game_phase"
params: none
available_game_phases: All
description: returns a string representing the current game phase
```

```
query_name: "time_until_start"
params: none
available_game_phases: ["waiting"]
description: returns the number seconds until the game starts
```

```
query_name: "get_players"
params: none
available_game_phases: All
description: returns a list containing data about each player
```

```
query_name: "my_turn?"
params: none
available_game_phases: ["placement", "playing"]
description: returns true if it is the calling players turn
```

```
query_name: "get_game_state"
params: none
available_game_phases: ["placement", "playing", "finished"]
description: returns a game state in the following format:
{
  players: [
    {
      color: "..."
      score: 0
      places: [[0,0], ...]
    },
    .
    .
  ]
  board: [ [1, 1, 2], ...]
}
```


```
query_name: "place_penguin"
params: [int, int]
available_game_phases: ["placement"]
description: asks the referee to place a penguin on a tile.
The tiles have the following layout:
   _____       _____       _____
  / 0,0 \_____/ 0,1 \_____/ 0,2 \_____
  \_____/ 1,0 \_____/ 1,1 \_____/ 1,2 \
  / 2,0 \_____/ 2,1 \_____/ 2,2 \_____/
  \_____/     \_____/     \_____/

```

```
query_name: "make_move"
params: [[int, int], [int ,int]]
available_game_phases: ["playing"]
description: asks the referee to take a turn by moving a penguin
from one tile to another. If the player gives an invalid move they are kicked
from the game.
The tiles have the following layout:
   _____       _____       _____
  / 0,0 \_____/ 0,1 \_____/ 0,2 \_____
  \_____/ 1,0 \_____/ 1,1 \_____/ 1,2 \
  / 2,0 \_____/ 2,1 \_____/ 2,2 \_____/
  \_____/     \_____/     \_____/

```

```
query_name: "get_my_valid_moves"
params: none
available_game_phases: ["playing"]
description: asks the referee to return a list of the calling players valid moves.
It is returned in the following format:
[[start_posn, end_posn], ....]

If they have no valid moves returns an empty list.
```

```
query_name: "query_move"
params: [[int, int], [int ,int]]
available_game_phases: ["playing"]
description: asks the referee to what the resukting game state would be
after making the given move. the format of the result is the same as described in
get_game_state.

 If the move is invalid it returns false
```

```
query_name: "game_over?"
params: none
available_game_phases: All
description: returns true if the game is in the finished state
```

```
query_name: "get_winner"
params: none
available_game_phases: "finished"
description: returns the color of the games winner
```


```
query_name: "get_my_color"
params: none
available_game_phases: All
description: returns the color the calling player is assigned
```

```
query_name: "quit"
params: none
available_game_phases: All
description: kicks yourself from the game
```
