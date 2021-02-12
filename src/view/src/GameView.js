import styled from 'styled-components';
import { Component } from 'react';
import Tournament from './Tournament';
import Game from './Game';

const ViewContainer = styled.div`
  display: flex;
  justify-content: space-around;
`;

class GameView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roundHistory: [
        [["Jing", "Max"], ["Steve", "Bess"], ["Bob", "Dug"]],
        [["Jing", "Steve"], ["Joel", "Dug"]],
        [["Jing", "Joel"]]
      ]
    }
  }

  render() {
    return (
      <ViewContainer>
        <Game />
        <Tournament roundHistory={this.state.roundHistory} />
      </ViewContainer>
    );
  }
}

export default GameView;