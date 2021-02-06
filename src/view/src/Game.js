import styled from 'styled-components';
import { Component } from "react";
import StatusPanel from './StatusPanel';
import Board from './Board';

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
    return (
      <GameInfo>
        <GameType>Checker</GameType>
        <GameState>
          <Board />
          <StatusPanel />
        </GameState>
      </GameInfo>
    );
  }
}

export default Game;