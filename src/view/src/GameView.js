import styled from 'styled-components';
import { Component } from 'react';
import Tournament from './Tournament';
import Game from './Game';

const ViewContainer = styled.div`
  display: flex;
  justify-content: space-around;
`;

class GameView extends Component {
  render() {
    return (
      <ViewContainer>
        <Game />
        <Tournament />
      </ViewContainer>
    );
  }
}

export default GameView;