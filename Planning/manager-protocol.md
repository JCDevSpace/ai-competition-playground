# Manager Protocol

A TournamentManager is a (Queue(Player), List[Observer], {TournamentId: TournamentStats})
The queue of players represents players waiting to join a tournament. This is a FIFO queue so that
the players who join earlier get into tournaments faster than players who join later.

The List of Observers represents the non-players that wish to watch games in a tournament.
An Observer is an object that holds a GameState that can be updated.

Finally, the map of TournamentId to TournamentStats represents the history of the tournaments.

A TournamentId is a int
This represents a uniquie id that gets assigned to a tournament when it begins

TournamentStats is a ([Player], [Player], [Players], [TournamentStats])
This tree like object represents the stats of each game in the tournament bracket.
The three lists of players in each node of the tree represent the winners, losers, and cheaters
of the game that node represents. The array of TournamentStats represents the stats of the 
games that the players won in order to advance to their parent node.

-----
## Interactions

#### Players
Players are added to the waiting queue by the tournament manager before the tournament begins.
They are passed to referees when it is time for them to play in a game.
The player adds themself to a the queue by calling the queue_player method on the TournamentManager

#### Referees
A referee is constructed by the tournament manager each time it needs to run a game of Fish. The tournament manager passes the players who will be competing in the game to the referee. Once the game has been run the 
referee returns a end game report of the winners, losers, and cheaters, so that the tournament manager
can keep track of these statistics.

#### Observers
Observers are added to the tournament manager so that they can watch the games that are happening. Observers add themselves to tournament by calling the add_observer method on the Tournament mangaer.

