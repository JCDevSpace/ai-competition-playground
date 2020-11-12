- The move penguin function from state failed to validate if it was turn of the player making the move
before making it. This resulted in a bug where if a move was made on the wrong players turn, the resulting
game state would be invalid.
fix: https://github.ccs.neu.edu/CS4500-F20/texarkana/commit/206a1bf492b20a2f519fd2f2dbb437342c29f1f9