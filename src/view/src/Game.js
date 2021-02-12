import styled from 'styled-components';
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

const State = styled.div`
  display: flex;
  width: 80em;
  justify-content: space-around;
`;

const Game = (props) => {
  return (
    <GameInfo>
      <GameType>{props.gameState.gameType}</GameType>
      <State>
        <CanvasBoard 
          tileSize={100} 
          gameType={props.gameState.gameType} 
          layout={props.gameState.layout} 
          avatars={props.gameState.avatars} 
        />
        <StatusPanel 
          players={props.gameState.players} 
          scores={props.gameState.scores}
        />
      </State>
    </GameInfo>
  );
}

export default Game;