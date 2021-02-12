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