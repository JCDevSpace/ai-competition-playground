## Self-Evaluation Form for Milestone 6

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

The implementation of the "steady state" phase of a board game
typically calls for several different pieces: playing a *complete
game*, the *start up* phase, playing one *round* of the game, playing a *turn*, 
each with different demands. The design recipe from the prerequisite courses call
for at least three pieces of functionality implemented as separate
functions or methods:

- the functionality for "place all penguins"
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/referee.py#L178-L183

- a unit test for the "place all penguins" funtionality 
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/UnitTests/RefereeTest.py#L114-L160

- the "loop till final game state"  function
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/referee.py#L164-L192

- this function must initialize the game tree for the players that survived the start-up phase
We chose to pass the player object the representation of a GameState (not the actual object that the referee uses) because we didnt feel it was necessary for the Referee to construct the Tree considering the main idea of the GameTree was for planning moves, which the referee doesn't do. IF the players want to plan their moves they can construct the GameTree themselves from the GameState that we gave them.
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/referee.py#L209-L214

- a unit test for the "loop till final game state"  function


- the "one-round loop" function
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/referee.py#L172-L190

- a unit test for the "one-round loop" function


- the "one-turn" per player function

https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/referee.py#L172-L190

- a unit test for the "one-turn per player" function with a well-behaved player 
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/UnitTests/RefereeTest.py#L162-L187

- a unit test for the "one-turn" function with a cheating player
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/UnitTests/RefereeTest.py#L214-L256


- a unit test for the "one-turn" function with an failing player 
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/UnitTests/RefereeTest.py#L189-L213

- for documenting which abnormal conditions the referee addresses 
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/referee.py#L19-L28

- the place where the referee re-initializes the game tree when a player is kicked out for cheating and/or failing 
We chose to pass the player object the representation of a GameState (not the actual object that the referee uses) because we didnt feel it was necessary for the Referee to construct the Tree considering the main idea of the GameTree was for planning moves, which the referee doesn't do. IF the players want to plan their moves they can construct the GameTree themselves from the GameState that we gave them.
https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish/Admin/referee.py#L209-L214


**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "7f602bd48bf50148dcf429664a9ee6ffeacec80f".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/wickett/tree/7f602bd48bf50148dcf429664a9ee6ffeacec80f/Fish>

