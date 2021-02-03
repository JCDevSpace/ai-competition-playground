import { Component } from 'react';
import MatchUp from './MatchUp';

class RoundCard extends Component {
  render() {
    return (
      <div>
        <h3>Round 1</h3>
        <MatchUp className="match-up" />
        <MatchUp className="match-up" />
      </div>
    );
  }
}

export default RoundCard;