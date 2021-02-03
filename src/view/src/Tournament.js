import { Component } from "react";
import RoundCard from './RoundCard'

class Tournament extends Component {
  render() {
    return (
      <div className="tournament-view">
        <h2>Tournament Rounds</h2>
        <div className="rounds">
          <RoundCard className="round-card" />
          <RoundCard className="round-card" />
        </div>
      </div>
    );
  }
}

export default Tournament;