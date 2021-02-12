import styled from 'styled-components';
import RoundCard from './RoundCard'

const TournamentInfo = styled.div`
  align-self: center;
  background-color: lightpink;
`;

const TournamentTitle = styled.h3`
  text-align: center;
  background-color: blueviolet;
`;

const RoundSlide = styled.div`
  overflow-y: scroll;
  height: 51em;
  background-color: lightgrey;
`;

const Tournament = (props) => {
  return (
    <TournamentInfo>
      <TournamentTitle>Tournament Rounds</TournamentTitle>
      <RoundSlide>
        {props.roundHistory.map((matchUps, index) => {
          return <RoundCard
            key={index}
            round={index + 1}
            matchUps={matchUps}
          />
        })}
      </RoundSlide>
    </TournamentInfo>
  );
}

export default Tournament;