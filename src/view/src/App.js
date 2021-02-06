import styled from 'styled-components';
import { Component } from 'react';
import GameView from './GameView';

const ViewContainer = styled.div`
  background-color: greenyellow;
`;

const Logo = styled.h2`
  float: top;
  width: fit-content;
  background-color: lightgoldenrodyellow;
`;

class App extends Component {
  render() {
    return (
      <ViewContainer>
        <Logo>AI Lab</Logo>
        <GameView />
      </ViewContainer>
    );
  }
}

export default App;
