import { Component } from 'react';
import Square from './Square';

class Board extends Component {
  renderTile() {
    return (
      <Square />
    );
  }

  render() {
    return (
      <div>
        <div className="board-row">
            {this.renderTile(0)}
            {this.renderTile(1)}
            {this.renderTile(2)}
        </div>
        <div className="board-row">
            {this.renderTile(3)}
            {this.renderTile(4)}
            {this.renderTile(5)}
        </div>
        <div className="board-row">
            {this.renderTile(6)}
            {this.renderTile(7)}
            {this.renderTile(8)}
        </div>        
      </div>
    );
  }
}

export default Board;