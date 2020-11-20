# Remote Collaboration Protocol

## Logical Interaction Diagram

```ASCCI
    +---------------------+     +---------------+
    |                     |     |   Server      |
    |   Remote Players    +-----+   Components  |
    |                     |     |   Proxy       |
    +---------------------+     +-------+-------+
                                        |
                                        |
                                        |
                                        |
+----------------------------------------------------------------------------------------------+
Network Boundary                        |
                                  +-----+------+          +-----------------------------------+
                                  |  Remote    |          |         Server Components         |
                                  |  Player    +----------+          +------------+           |
                                  |  Proxy     |          |          |            |           |
                                  +------------+          |          |   Referee  |           |
                                                          |          |            |           |
                                                          |          +------------+           |
                        +----------------------+          |    +--------------------------+   |
                        |                      |          |    |                          |   |
                        |   House AI Players   +----------+    |     Tournament Manager   |   |
                        |                      |          |    |                          |   |
                        +----------------------+          |    +--------------------------+   |
                                                          +-----------------------------------+


```

## Components and Interaction Description

### Communication between Server Components and Local Players

In the current implementation, the server components such as the referee and the tournament manager interact with house AI players that impelent the Player Interface. These components communicate with the house players by calling a method called `send_message` on the object. A server component builds a python dictionary in the following format to send to player implentations that contains the type of message and the data associated with that request:

```Python
{
    type: "message_type"
    content: ...
}
```

The `send_message` method on the player returns the requested data or acknowledgement of the message depending on the information in this message the server component sends to the house player.

### Communication between Server Components and Remote Players

To extend this behavior of requesting responses from a player across a network boundary, we will implement a Remote Player Proxy. The server components will treat this object exactly like a House AI, but the Remote Player Proxy will write messages across a TCP connection to get responses from a remote player.

The Remote Player Proxy will acheive this by encoding the messages passed to it by the `send_message` method as JSON's and writing that message to a TCP socket. On the other side of this socket will be a Server Component Proxy that reads from the TCP socket and decodes the json. The Server Component Proxy will then call the `send_message` method on the Remote Player and pass in the decoded message.

The Server Component Proxy will then take the return value of the `send_message` call and encode it as a json. Next, it writes the encoded json back over the TCP socket so that the Remote Player Proxy can decode this value, and pass the Remote Player's response back to the Server Components.

These will be the formats of the json's that are written across the TCP connection:

```JSON

Request
{
    "type": json string
    "content": json object
}

Response:
{
    "response": json object
}
```

In this manner the Server Components will be able to send data back and forth to the remote players.
