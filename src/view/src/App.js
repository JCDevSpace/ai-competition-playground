import styled from 'styled-components';
import { Component } from 'react';
import GameView from './GameView';
import WebSocketClient from './WebSocketClient'

const ViewContainer = styled.div`
  background-color: greenyellow;
`;

const Logo = styled.h2`
  margin: 0;
  width: fit-content;
  background-color: lightgoldenrodyellow;
`;

class App extends Component {
  render() {
    return (
      // <ViewContainer>
      //   <Logo>Logo</Logo>
      //   <GameView />
      // </ViewContainer>
      <WebSocketClient />
    );
  }
}

export default App;
