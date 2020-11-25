# Todo List

## Board

[x] Reachable tiles purpose statement need to state what it means to be "reachable" in this context
(in straight line, no holes or other penguins)

---

## Game State

[x] We need to add unit test around what should happen if a player makes a move when it is not their turn
vs when it is their turn. There is also a bug if a player makes a turn when its not their turn

[x] Change our player representation in the game state from (Color, Age) to just Color. This is because the referee is supposed to contain information about the age and turn order rather than the GameState. We will also need to fix the unit test according to the changes.

---

## FishView

[x] Failing unit tests to calculate frame width and height

---

## Game Tree

[x] We need to specify what different nodes in our game tree look like in comments. We need to distinguish
 a node where a player can move penguins vs when a player's turn is skipped vs when the game is over.

---

## Player

[x] We have unused methods our Player class and comments that don't match what the code does

---

## Refree

[] Seperate function to handle placement and movement phase of the game

[] The refree does not make use of a game tree to do rule checks

[] Seperate function for calls to player that provides protection for any exceptions or timing out

[] Missing unit test for running game to completion and covering all abnormal conditions

[] Pass in the board configuration to referee as hash

[] Work around defensive programming in referee constructor

[] Put color assignment into a seperate function

---
