import { Component } from 'react';
import Tournament from './Tournament';
import Game from './Game';

class App extends Component {
  render() {
    return (
      <div className="view-container">
        <h1 className="logo">AI LAB</h1>
        <Game className="game" />
        <Tournament className="tournament" />
      </div>
    );
  }
}

export default App;
