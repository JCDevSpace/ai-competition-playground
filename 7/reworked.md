- Change our player representation from (Color, Age) to just Color
In our initial data representation for a player in the gamestate we thought we would also
need to inculde other data abour players like their age, however the referee should
hold this information and not the gamestate, so we changed everywhere that we used the
old Player object to just a string representing the color for that player. This had a lot of
fanout because we used the Player class in a lot of places in the code base.

https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/f584934c4776c660a7a60c7ced1f96660b097f10
