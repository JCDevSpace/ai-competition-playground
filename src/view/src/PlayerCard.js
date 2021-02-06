import styled from 'styled-components';

const PlayerInfo = styled.div`
  padding: 1em;
  border-radius: 2em;
  align-self: center;
  width: fit-content;
  background-color: yellow;
`;

function PlayerCard(prop) {
  return (
    <PlayerInfo>
      Name: Jing<br />
      Color: Red<br />
      Score: 10<br />
    </PlayerInfo>
  );
}

export default PlayerCard;