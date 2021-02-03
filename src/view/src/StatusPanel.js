import { Component } from 'react';
import PlayerCard from './PlayerCard';

class StatusPanel extends Component {
  render() {
      return (
        <div className="game-status-view">
          <PlayerCard clasName="player-card" />
          <PlayerCard clasName="player-card" />
        </div>
      );
    }
}

export default StatusPanel;