import styled from 'styled-components';

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
    players.push(<div key={player}>{player} </div>) 
  }

  return (
    <MatchUpInfo>
      {players}
    </MatchUpInfo>
  );
}

export default MatchUp;