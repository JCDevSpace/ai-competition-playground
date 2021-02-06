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

function RoundCard(prop) {
  return (
    <RoundContainer>
      <RoundCount>Round {prop.round}</RoundCount>
      <MatchUps>
        <MatchUp players={["Jing", "Max", "Adrian"]} />
        <MatchUp players={["Bob", "Dug"]} />
      </MatchUps>
    </RoundContainer>
  );
}

export default RoundCard;