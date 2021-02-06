import styled from 'styled-components';
import { Component } from 'react';
import Tile from './Tile';

const BoardGrid = styled.div`
  height: fit-content;
  background-color: lightblue;

  &:after {
    clear: both;
    content: "";
    display: table;
  }
`;

class Board extends Component {
  renderTile() {
    return (
      <Tile />
    );
  }

  render() {
    return (
      <BoardGrid>
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
      </BoardGrid>
    );
  }
}

export default Board;