import styled from 'styled-components';

const MatchUpInfo = styled.div`
  padding: 2em;
  border-radius: 4em;
  align-self: center;
  text-align: center;
  width: fit-content;
  background-color: yellow;
`;

const MatchUp = (props) => {
  return (
    <MatchUpInfo>
      {props.players.map((player, index) => {
        return <div key={index}>{player}</div>
      })}
    </MatchUpInfo>
  );
}

export default MatchUp;