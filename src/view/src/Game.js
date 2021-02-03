import { Component } from "react";
import StatusPanel from './StatusPanel';
import Board from './Board';

class Game extends Component {
  render() {
    return (
      <div className="game-view">
        <h2 className="game-type">Checker</h2>
        <Board className="board" />
        <StatusPanel className="status-panel" />
      </div>
    );
  }
}

export default Game;