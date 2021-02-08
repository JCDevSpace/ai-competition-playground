import styled from 'styled-components';
import { Component } from "react";
import StatusPanel from './StatusPanel';
import Board from './CanvasBoard';

const GameInfo = styled.div`
  background-color: violet;
`;

const GameType = styled.h3`
  float: top;
  margin-top: 0;
  width: fit-content;
  background-color: lightcoral;
`;

const GameState = styled.div`
  display: flex;
  width: 80em;
  justify-content: space-around;
`;

class Game extends Component {
  render() {
    const testLayout = [
      [0,1,0,1,0,1,0,1],
      [1,0,1,0,1,0,1,0],
      [0,1,0,1,0,1,0,1],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [1,0,1,0,1,0,1,0],
      [0,1,0,1,0,1,0,1],
      [1,0,1,0,1,0,1,0]
    ];
    return (
      <GameInfo>
        <GameType>Checker</GameType>
        <GameState>
          <Board layout={testLayout}/>
          <StatusPanel />
        </GameState>
      </GameInfo>
    );
  }
}

export default Game;