## Self-Evaluation Form for Milestone 8

Indicate below where your TAs can find the following elements in your strategy and/or player-interface modules:

1. did you organize the main function/method for the manager around
the 3 parts of its specifications --- point to the main function

Yes, our main function first informs the players the tournament starts, runs the tournament, and informs the players if they won.

https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/97afe956bd59274e861e8ed204987adbe622fe3d/Fish/Admin/manager.py#L42:L58

2. did you factor out a function/method for informing players about
the beginning and the end of the tournament? Does this function catch
players that fail to communicate? --- point to the respective pieces

Yes, it catches errors thrown by the call to the player object.

https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/97afe956bd59274e861e8ed204987adbe622fe3d/Fish/Admin/manager.py#L137:L144


3. did you factor out the main loop for running the (possibly 10s of
thousands of) games until the tournament is over? --- point to this
function.

No, we need to move the following lines into a separate function.

https://github.ccs.neu.edu/CS4500-F20/texarkana/blob/97afe956bd59274e861e8ed204987adbe622fe3d/Fish/Admin/manager.py#L45:L54

**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**


  WARNING: all perma-links must point to your commit "97afe956bd59274e861e8ed204987adbe622fe3d".
  Any bad links will be penalized.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/texarkana/tree/97afe956bd59274e861e8ed204987adbe622fe3d/Fish>

