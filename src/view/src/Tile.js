import styled, {css} from 'styled-components';
import { Component } from 'react';

const SquareTile = styled.div`
  background: transparent;
  border: 1px solid #999;
  float: left;
  font-size: 24px;
  font-weight: bold;
  line-height: 34px;
  height: 34px;
  margin-right: -1px;
  margin-top: -1px;
  padding: 0;
  text-align: center;
  width: 34px;
`;

const DiamondTile = styled.div`
  width: 0;
  height: 0;
  border: 50px solid transparent;
  border-bottom: 70px solid red;
  position: relative;
  top: -50px;

  &:after {
    content: '';
    position: absolute;
    left: -50px;
    top: 70px;
    width: 0;
    height: 0;
    border: 50px solid transparent;
    border-top: 70px solid orange;
  }
`;

const ShapedTile = styled.div`
  ${(props) =>
    props.shape === "sqaure" &&
    css`
      background: #fff;
      border: 1px solid #999;
      float: left;
      font-size: 24px;
      font-weight: bold;
      line-height: 34px;
      height: 34px;
      margin-right: -1px;
      margin-top: -1px;
      padding: 0;
      text-align: center;
      width: 34px;
    `
  }

  ${(props) =>
    props.shape === "diamond" &&
    css`
      width: 0;
      height: 0;
      border: 50px solid transparent;
      border-bottom: 70px solid red;
      position: relative;
      top: -50px;

      &:after {
        content: '';
        position: absolute;
        left: -50px;
        top: 70px;
        width: 0;
        height: 0;
        border: 50px solid transparent;
        border-top: 70px solid orange;
      }
    `
  }
`;


class Tile extends Component {
  render() {
    return (
      // <ShapedTile shape="square">X</ShapedTile>
      // <DiamondTile />
      <SquareTile />
    );
  }
}

export default Tile;