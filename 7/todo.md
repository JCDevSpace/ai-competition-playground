# Game State
[X] We need to add unit test around what should happen if a player makes a move when it is not their turn
vs when it is their turn. There is also a bug if a player makes a turn when its not their turn

[x] Change our player representation from (Color, Age) to just Color. This is because the referee is supposed to contain information about the age and turn order rather than the GameState. We will also need to fix the unit test according to the changes.

# Game Tree
[] We need to specify what different nodes in our game tree look like in comments. We need to distinguish
 a node where a player can move penguins vs when a player's turn is skipped vs when the game is over.

# Player
[] We have unused methods our Player class and comments that don't match what the code does
