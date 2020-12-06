# Remote

This directory contains the client and server components of Fish.

---

## File Organization

In this directory we have 4 files. The `client.py` file contains the client,
that is created with a remote_player to receive messages from, and a
client player to pass the messages to. Ther `server.py` file contains the server,
which accepts signups. If enough signups are received, it creates a tournament
manager that runs a tournament for all the players. The `messages.py` file stores
stores the constants used in Messages between the client and server. It also
contains methods for converting internal representations to Formatted representationsa
The `remote_player.py` file is a type of Player that can be given to the Referee,
which acts as a proxy, allowing communication between the client and Referee.

---

## Modified pieces of code