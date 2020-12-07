# Remote

This directory contains the client and server components of Fish.

---

## File Organization

In this directory we have 4 files. The `client.py` file contains the client,
that is created with a remote_player to receive messages from, and a
client player to pass the messages to. The `server.py` file contains the server,
which accepts signups. If enough signups are received, it creates a tournament
manager that runs a tournament for all the players. The `messages.py` file stores
stores the constants used in Messages between the client and server. It also
contains methods for converting internal representations to Formatted representationsa
The `remote_player.py` file is a type of Player that can be given to the Referee,
which acts as a proxy, allowing communication between the client and Referee.

---

## Modified pieces of code

### Manager.py

- Made it so the Manager can take an observer to give to the Referee, useful for debugging with game visualization
- Manager now keeps track of the list of all cheating/failing (kicked) players
- Fixed a bug in manager so we don't attempt to communicate with all cheating/failing players after they get kicked
- Manager now kicks players who fails when informed the start of the tournament
- Manager now returns the winners and kicked players, whereas before it returned just the winners

### Referee.py

- Referee now returns winning and kicked players, used to just return the winning players