## Self-Evaluation Form for Milestone 7

Please respond to the following items with

1. the item in your `todo` file that addresses the points below.
    It is possible that you had "perfect" data definitions/interpretations
    (purpose statement, unit tests, etc) and/or responded to feedback in a 
    timely manner. In that case, explain why you didn't have to add this to
    your `todo` list.

2. a link to a git commit (or set of commits) and/or git diffs the resolve
   bugs/implement rewrites: 

These questions are taken from the rubric and represent some of the most
critical elements of the project, though by no means all of them.

(No, not even your sw arch. delivers perfect code.)

### Board

- a data definition and an interpretation for the game _board_

We had no feedback for anything wrong with our Board interpretation. At some point early
in the assignment me and my previous partner did make some changes to fix old feedback
but they were strewn across several commits.

For the current state of our board interpretation see: https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/15bb8e8ed31bcaec0eddf59acdc3f7945fa66a0b/Fish/Common/board.py#L4-L29

- a purpose statement for the "reachable tiles" functionality on the board representation

Our code base correctly addressed the reachable tiles functionality.

For the current state of our reachable tiles functionality see: https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/15bb8e8ed31bcaec0eddf59acdc3f7945fa66a0b/Fish/Common/board.py/#L157-L159

- two unit tests for the "reachable tiles" functionality

We had unit test around our reachable tiles functionality.

For the current states of these tests see: https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/15bb8e8ed31bcaec0eddf59acdc3f7945fa66a0b/Fish/Common/UnitTests/BoardTest.py#L65-L77

### Game States 


- a data definition and an interpretation for the game _state_

We had an item in our todo file to change the representaion of a player in the state. We changed it from
a python object to a string that is one of the 4 colors allowed in the game. These are the changes we made to address this change we wanted to make.

https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/f584934c4776c660a7a60c7ced1f96660b097f10

- a purpose statement for the "take turn" functionality on states

Our current code base accurately described the take turn functionality in the game state.

For the current state of the "take turn" functionality see: https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/15bb8e8ed31bcaec0eddf59acdc3f7945fa66a0b/Fish/Common/state.py#L101-L105

- two unit tests for the "take turn" functionality

We had an item in our todo list for the missing unit test for a player taking a turn when it is not their turn. This also revealed a bug in our code that leaves the state object in an inconsistent state if this illegal move is attempted.

We added a extra test for this in the following commit:
https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/206a1bf492b20a2f519fd2f2dbb437342c29f1f9


### Trees and Strategies


- a data definition including an interpretation for _tree_ that represent entire games

We had an item in our todo list to clarify what different nodes in the game tree looked like. We got feedback
that it was unclear what the difference between nodes where a player can make a move vs needing to have their turn skipped vs the game being over.

We added an extra comment to explain these nodes in the following commit:

https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/4a189b63fd669e59d12d2179ff718df5a696de17

- a purpose statement for the "maximin strategy" functionality on trees

Our code base correctly addressed this maximin strategy purpose statement.

For the current state of the purpose statement see: https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/15bb8e8ed31bcaec0eddf59acdc3f7945fa66a0b/Fish/Player/strategy.py#L45:L47

- two unit tests for the "maximin" functionality 

Our code base had enough units around the maximin strategy

For the current state of these tests see: https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/15bb8e8ed31bcaec0eddf59acdc3f7945fa66a0b/Fish/Player/UnitTests/StrategyTest.py#L69:L124




### General Issues

Point to at least two of the following three points of remediation: 


- the replacement of `null` for the representation of holes with an actual representation 

Our code base correctly addressed this hole representation, by using 0 for a hole instead of null.

To see the current state of the hole representations see: https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/15bb8e8ed31bcaec0eddf59acdc3f7945fa66a0b/Fish/Common/board.py#L15



- one name refactoring that replaces a misleading name with a self-explanatory name

In our state object we had a method called "get_current_player()." This method returned the player object whose turn it was. We renamed this to "get_current _color()" because we changed our data representation of a state to use colors instead of player object to represent the players in the game.

We changed this in the following commit: 

https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/f584934c4776c660a7a60c7ced1f96660b097f10

- a "debugging session" starting from a failed integration test:
  - the failed integration test
  - its translation into a unit test (or several unit tests)
  - its fix
  - bonus: deriving additional unit tests from the initial ones 


### Bonus

Explain your favorite "debt removal" action via a paragraph with
supporting evidence (i.e. citations to git commit links, todo, `bug.md`
and/or `reworked.md`).



