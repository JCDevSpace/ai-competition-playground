# Referee

A Referee is a (GameState,  Map{AuthToken : Player}, List[Player])

Where the GameState represents the current state of the game

The mapping from AuthToken to Player represents a way to 
identify an incoming message as coming from a certain player.

` An AuthToken is a String representing a unique authentication id given to players when they connect to the service`

The List of Players represents the current list of Players who have been kicked for either cheating for failing.

The GameState stored in the Referee is the "ground truth", 
if players edit their own GameStates it does not affect the 
true state of the game which is held by the Referee. 

As players make requests to the Referee, this true GameState will
be updated assuming the players made valid moves.



## API

```
# Creates a Referee given the AuthTokens and ages of all the players who will be a part of the game.
# This generates the information needed to run a game of Fish,
# including creating a Board with either the given or randomized specifications.
# By initializing this object the Game as entered into the "placement" Phase, and has started.
__init__(List[(AuthToken, Age)], size=(Int, Int), holes=List[Position], num_one_fish=Int, num_holes=Int) -> Referee


----- Public Methods
# A GamePhase is one of
# - "placement"
# - "playing"
# - "finished"
# This represents what part of the game is happening at a given moment

# Gets the current GamePhase of this instance of Hey Thats my Fish
# Usable in all GamePhases
get_game_phase() -> GamePhase 

#Returns wether or not the palyer corresponding to the given AuthToken is kicked
is_kicked(AuthToken) -> Boolean

# Returns the list of players who are playing in this instance of Fish
# Usable in all GamePhases
get_players() -> List[Player]

# Returns the color of the player with the given AuthToken,
# returns False if it is an invalid AuthToken
# Only usable in "placement" or "playing" GamePhases
get_color(AuthToken) -> Color

# Returns the color of the player who's turn it is.
# Only usable in "placement" or "playing" GamePhases
get_whos_turn() -> Color

# Returns a copy of the current true GameState.
# Usable in "placement", "playing", or "finished" GamePhases.
get_game_state() -> GameState

# If the GamePhase is "placement" and it is the calling players turn,
# places a penguin at the given position
# Returns True if successful, if unsuccessful returns False
# and the player is kicked
place_penguin(AuthToken, Position) -> Boolean

# If the GamePhase is "playing" and it is the calling players turn, it makes that move
# from the first Position to the second.
# Returns True if successful, if unsuccessful returns False
# and the player is kicked
make_move(AuthToken, Position, Position) -> Boolean

# If the GamePhase is "playing"
# then this returns a list of the player's valid moves
def get_my_valid_moves(AuthToken): -> List[Move]

# If the GamePhase is "finished" then it
# returns the color of the winner is
def get_winner() -> Color

# This shuts down the game. This will be called by the Tournament Manager 
# if the game should be terminated early or if the game ends.
# this retruns the winner and the list of cheaters/failures 
def shutdown() -> Player, List[Player]



----Private Methods

# Kicks the given player from the game. This means all of their penguins are removed from
# the board and they are not allowed to make any moves.
# They are added the the list of kicked player, which will be reported back
# after the end of the game.
kick(AuthToken) -> Void


# Determines which player a given AuthToken belongs to.
# Usable in all GamePhases.
determine_player(AuthToken) -> Player


```

## How the other components interact with the Referee

The Tournament Manager will initialize Referee objects each time a new game of Fish should begin.

As the players request to the server their moves, they are parsed and sent to the referee which will
modify the GameState if needed. and return key information. 
Based on the response from the Referee to the server a 
responding message will be sent back to the player who made the request.

 