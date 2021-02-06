import styled from 'styled-components';
import { Component } from 'react';
import PlayerCard from './PlayerCard';

const StatusContainer = styled.div`
  width: 20%;
  height: 30em;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  background-color: lightcoral;
`;

class StatusPanel extends Component {
  render() {
      return (
        <StatusContainer>
          <PlayerCard />
          <PlayerCard />
        </StatusContainer>
      );
    }
}

export default StatusPanel;