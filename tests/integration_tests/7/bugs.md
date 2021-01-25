### Untested behavior when moving penguins in gamestate
The move penguin function from state failed to validate if it was turn of the player making the move
before making it. This resulted in a bug where if a move was made on the wrong players turn, the resulting
game state would be invalid.  
fix: https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/206a1bf492b20a2f519fd2f2dbb437342c29f1f9

### Calculating view frame width incorrectly
The number of rows determines height and the number of columns determines width. We had it the other way around in our calculations. We also forgot to remove a call to a method we deleted. Also the relative imports were broken in referee so we fixed those
so we could visulaly verify our view was working correctly.  
fix: https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/1c38852558491b92a104bb49e4d268326a55d6ec