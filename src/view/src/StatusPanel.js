import styled from 'styled-components';
import PlayerCard from './PlayerCard';

const StatusContainer = styled.div`
  width: 20%;
  height: 30em;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  background-color: lightcoral;
`;

const StatusPanel = (props) => {
  return (
    <StatusContainer>
      {props.players.map((color, index) => {
        return <PlayerCard 
          key={index + color}
          currentPlayer={index === 0} 
          color={color} 
          score={props.scores[color]}
        />
      })}
    </StatusContainer>
  );
}

export default StatusPanel;