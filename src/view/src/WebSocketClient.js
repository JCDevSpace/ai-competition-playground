import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from "websocket";

const client = new W3CWebSocket('ws://127.0.0.1:8000');

class WebSocketClient extends Component {
  componentDidMount() {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
      client.send(JSON.stringify({'msg-type': "observe", 'content': "webobserver"}));
    };
    client.onmessage = (message) => {
      console.log(message.data);
    };
    client.onclose = (message) => {
      console.log("Connection close from server with message", message.data);
    }
  }

  sentUpdate() {
    client.send("Update!!!");
  }

  sentClose() {
    client.send("Bye server!");
  }
  
  render() {
    return (
      <div>
        <button onClick={this.sentUpdate} >Sent Update</button>
        <br />
        <button onClick={this.sentClose} >Close Connection</button>
      </div>
    );
  }
}

export default WebSocketClient;