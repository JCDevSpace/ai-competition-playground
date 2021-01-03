# Board Game AI

This project aims to design and implement a tournament system that allows AIs implemented on the specified protocol to compete with each other in different board games, and through doing so, learn about the various fundamental AI algorithms. This is build on top of the original project from my [software development course](https://felleisen.org/matthias/4500-f20/assignments.html) in [Northeastern University](https://www.northeastern.edu/), where the original system was designed only for the board game Fish, with the core components implemented in Python. This continuation of the project will aim to implement the rest of the fundamental AI algorithms as specified in [todo.md](https://github.com/JCDevSpace/board-game-ai/blob/master/todo.md#ai-algorithms) aside from the original MiniMax algorithm. In addition, a new web front end will be added to allow the ease of spectating for the games.

## Installation

Clone the project repo to the local system.

To run a quick test to verify that the project is working properly on the local system.  

```bash
cd ~/board-game-ai
./xtest
```

This will run all the unittests and integration tests under the `Test` directory of the repo.

## Usage

To run a tournament server.

```bash
./xserver
```

This will start up a server process that sit and waits for signups to participate in the a tournament.

To start up a client.

```bash
./xclient
```

This will start up a client process that uses a defalut in house developed player to participate in a tournament.  
