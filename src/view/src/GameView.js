import { w3cwebsocket as W3CWebSocket } from "websocket";
import styled from 'styled-components';
import { Component } from 'react';
import Tournament from './Tournament';
import Game from './Game';
import { decode, valid_type } from "./Message";

const ViewContainer = styled.div`
  display: flex;
  justify-content: space-around;
`;

class GameView extends Component {
  constructor(props) {
    super(props);
    this.responder_table = {
      T_START: this.t_start_update,
      T_PROGRESS: this.t_progress_update,
      T_END: this.t_end_update,
      G_START: this.g_start_update,
      G_ACTION: this.g_action_update,
      G_KICK: this.g_kick_update
    }
    this.client = new W3CWebSocket('ws://127.0.0.1:8000');
    this.state = {
      active_players: [],
      roundHistory: [
        [["Jing", "Max"], ["Steve", "Bess"], ["Bob", "Dug"]],
        [["Jing", "Steve"], ["Joel", "Dug"]],
        [["Jing", "Joel"]]
      ],
      currentGame: {
        players: [
          "azure", "crimson"
        ],
        scores: {
          "crimson": 20,
          "azure": 10
        },
        gameType: "checker",
        layout: [
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]
        ],
        avatars: {
          "crimson": [[5, 0], [5, 2], [5, 4], [5, 6], 
            [6, 1], [6, 3], [6, 5], [6, 7], 
            [7, 0], [7, 2], [7, 4], [7, 6]],
          "azure": [[0, 0],[0, 1], [0, 3], [0, 5], [0, 7], 
            [1, 0], [1, 2], [1, 4], [1, 6], 
            [2, 1], [2, 3], [2, 5], [2, 7]],
        }
      }
    }
  }

  componentDidMount() {
    this.client.onopen = () => {
      console.log('WebSocket this.client Connected');
      this.client.send(JSON.stringify({'msg-type': "observe", 'content': "web"}));
    }

    this.client.onmessage = (event) => {
      this.process_message(event.data);
    }

    this.client.onclose = (event) => {
      console.log("Connection close from server with message", event.data);
    }
  }

  process_message(msg) {
    try {
      const {msg_type, content} = decode(msg);
      if (valid_type(msg_type)) {
        const handler = this.responder_table[msg_type];
        handler(content);
      }
    } catch (error) {
      console.log(error, "while processing message");
    }
  }

  t_start_update(players) {
    console.log("Received t start", players);
    // let state = this.state;
    // state.active_players = players;
    // this.setState(state);
  }

  t_progress_update(round_result) {
    console.log("Received t progress", round_result);
    // this.setState();
  }

  t_end_update(winners) {
    console.log("Received t end", winners);
    // this.setState();
  }

  g_start_update(game_state) {
    console.log("Received g start", game_state);
    // this.setState();
  }

  g_action_update(action) {
    console.log("Received g action", action);
    // this.setState();
  }

  g_kick_update(player) {
    console.log("Received g kick", player);
    // this.setState();
  }

  render() {
    return (
      <ViewContainer>
        <Game gameState={this.state.currentGame} />
        <Tournament roundHistory={this.state.roundHistory} />
      </ViewContainer>
    );
  }
}

export default GameView;