import styled from 'styled-components';
import PlayerCard from './PlayerCard';

const MatchUpInfo = styled.div`
  padding: 2em;
  border-radius: 4em;
  align-self: center;
  text-align: center;
  width: fit-content;
  background-color: yellow;
`;

function MatchUp(prop) {
  let players = [];

  for (const player of prop.players) {
    players.push(<objectRow>{player} </objectRow>) 
  }

  return (
    <MatchUpInfo>
      {players}
    </MatchUpInfo>
  );
}

export default MatchUp;