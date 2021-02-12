import styled from 'styled-components';
import { Component } from "react";
import StatusPanel from './StatusPanel';
import CanvasBoard from './CanvasBoard';

const GameInfo = styled.div`
  background-color: violet;
`;

const GameType = styled.h3`
  float: top;
  margin-top: 0;
  width: fit-content;
  text-transform: capitalize;
  background-color: lightcoral;
`;

const GameState = styled.div`
  display: flex;
  width: 80em;
  justify-content: space-around;
`;

class Game extends Component {
  constructor(props) {
    super(props);
    this.state = {
      players: [
        "azure", "crimson"
      ],
      scores: {
        "crimson": 20,
        "azure": 10
      },
      gameType: "fish",
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

  render() {
    return (
      <GameInfo>
        <GameType>{this.state.gameType}</GameType>
        <GameState>
          <CanvasBoard 
            tileSize={100} 
            gameType={this.state.gameType} 
            layout={this.state.layout} 
            avatars={this.state.avatars} 
          />
          <StatusPanel 
            players={this.state.players} 
            scores={this.state.scores}
          />
        </GameState>
      </GameInfo>
    );
  }
}

export default Game;