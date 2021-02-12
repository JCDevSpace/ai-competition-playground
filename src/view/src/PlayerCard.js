import styled from 'styled-components';

const PlayerInfo = styled.div`
  padding: 1em;
  border: 1px solid ${props => props.isCurrent? `black` : `lightgreen`};
  border-radius: 2em;
  align-self: center;
  width: fit-content;
  background-color: lightgreen;
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