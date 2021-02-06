import styled from 'styled-components';
import { Component } from "react";
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

class Tournament extends Component {
  render() {
    return (
      <TournamentInfo>
        <TournamentTitle>Tournament Rounds</TournamentTitle>
        <RoundSlide>
          <RoundCard round={1} />
          <RoundCard round={2} />
          <RoundCard round={3} />
          <RoundCard round={4} />
          <RoundCard round={5} />
        </RoundSlide>
      </TournamentInfo>
    );
  }
}

export default Tournament;