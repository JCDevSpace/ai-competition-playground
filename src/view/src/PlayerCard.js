import styled from 'styled-components';

const PlayerInfo = styled.div`
  padding: 1em;
  border: 1px solid ${props => props.isCurrent? `white` : `green`};
  border-radius: 2em;
  align-self: center;
  width: fit-content;
  background-color: green;
`;

const PlayerCard = (props) => {
  return (
    <PlayerInfo isCurrent={props.currentPlayer}>
      Color: {props.color}<br />
      Score: {props.score}<br />
    </PlayerInfo>
  );
}

export default PlayerCard;