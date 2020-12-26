###  Change our player representation from (Color, Age) to just Color
In our initial data representation for a player in the gamestate we thought we would also
need to inculde other data abour players like their age, however the referee should
hold this information and not the gamestate, so we changed everywhere that we used the
old Player object to just a string representing the color for that player. This had a lot of
fanout because we used the Player class in a lot of places in the code base.
https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/f584934c4776c660a7a60c7ced1f96660b097f10

---

###  Unclear data representation documentation in GameTree
We added more comments to clarify what different nodes in the game tree will look like.  
https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/4a189b63fd669e59d12d2179ff718df5a696de17

---

###  Unused code in Player
We deleted the unused code.  
https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/a5ccf90a62bb1c66d6eb05054ec7751873b5380d