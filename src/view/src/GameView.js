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
      activePlayers: [],
      roundHistory: [
        [["Jing", "Max"], ["Steve", "Bess"], ["Bob", "Dug"]],
        [["Jing", "Steve"], ["Joel", "Dug"]],
        [["Jing", "Joel"]]
      ],
      currentGame: {
        players: [],
        scores: {},
        gameType: null,
        layout: [[]],
        avatars: {}
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
        handler(this, content);
      }
    } catch (error) {
      console.log(error, "while processing message");
    }
  }

  t_start_update(self, players) {
    self.setState({
      activePlayers: players,
      roundHistory: self.state.roundHistory,
      currentGame: {
        players: self.state.currentGame.players,
        scores: self.state.currentGame.scores,
        gameType: self.state.currentGame.gameType,
        layout: self.state.currentGame.layout,
        avatars: self.state.currentGame.avatars
      }
    });
  }

  t_progress_update(self, round_result) {
    console.log("Received t progress", round_result);
    // this.setState();
  }

  t_end_update(self, winners) {
    console.log("Received t end", winners);
    // this.setState();
  }

  g_start_update(self, game_state) {
    console.log(game_state)
    const board_state = game_state.info.board.info;
    self.setState({
      activePlayers: self.state.activePlayers,
      roundHistory: self.state.roundHistory,
      currentGame: {
        players: game_state.info.players,
        scores: game_state.info.scores,
        gameType: game_state.info.board["board-type"],
        layout: board_state.layout,
        avatars: board_state.avatars
      }
    });
  }

  g_action_update(self, game_state) {
    const board_state = game_state.info.board.info;
    self.setState({
      activePlayers: game_state.info.board["board-type"],
      roundHistory: self.state.roundHistory,
      currentGame: {
        players: game_state.info.players,
        scores: game_state.info.scores,
        gameType: self.state.currentGame.gameType,
        layout: board_state.layout,
        avatars: board_state.avatars
      }
    });
  }

  g_kick_update(self, player) {
    console.log("Received g kick", player);
    const activePlayers = self.self.state.activePlayers.slice()
    const index = activePlayers.indexOf(player);
    activePlayers.splice(index, 1);
    self.setState({
      activePlayers: activePlayers,
      roundHistory: self.state.roundHistory,
      currentGame: {
        players: self.state.currentGame.players,
        scores: self.state.currentGame.scores,
        gameType: self.state.currentGame.gameType,
        layout: self.state.currentGame.layout,
        avatars: self.state.currentGame.avatars
      }
    });
  }

  render() {
    return (
    <ViewContainer>
      <Game gameState={this.state.currentGame} />
      <Tournament roundHistory={this.state.roundHistory} />
    </ViewContainer>);
  }
}

export default GameView;