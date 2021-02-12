import styled from 'styled-components';
import MatchUp from './MatchUp';

const RoundContainer = styled.div`
  margin: 7em;
  border: 2px solid;
  background-color: darkgrey;
`;

const RoundCount = styled.h4`
  background-color: gray;
`;

const MatchUps = styled.div`
  display: flex;
  flex-wrap: row;
  justify-content: space-evenly;
  background-color: lightblue;
`;

const RoundCard = (props) => {
  return (
    <RoundContainer>
      <RoundCount>Round {props.round}</RoundCount>
      <MatchUps>
        {props.matchUps.map((players, index) => {
          return <MatchUp 
            key={index}
            players={players}
          />
        })}
      </MatchUps>
    </RoundContainer>
  );
}

export default RoundCard;