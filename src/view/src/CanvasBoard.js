import styled from 'styled-components';
import { useEffect, useRef } from 'react';

const BoardCanvas = styled.canvas`
  width: ${props => props.width + "px"};
  height: ${props => props.height + "px"};
  border: 1px solid black;
`;

const getPixelRatio = context => {
  let backingStore =
  context.backingStorePixelRatio ||
  context.webkitBackingStorePixelRatio ||
  context.mozBackingStorePixelRatio ||
  context.msBackingStorePixelRatio ||
  context.oBackingStorePixelRatio ||
  context.backingStorePixelRatio ||
  1;
  
  return (window.devicePixelRatio || 1) / backingStore;
};

const Board = (props) => {
  const { layout, avatars} = props;

  const ref = useRef();

  const tileWidth = 100;
  const tileHeight = 100;

  const canvasWidth = layout.length * tileWidth;
  const canvasHeight = layout[0].length * tileHeight;

  useEffect(() => {
    let canvas = ref.current;
    let ctx = canvas.getContext('2d');
  
    let ratio = getPixelRatio(ctx);
    let width = getComputedStyle(canvas)
        .getPropertyValue('width')
        .slice(0, -2);
    let height = getComputedStyle(canvas)
        .getPropertyValue('height')
        .slice(0, -2);
      
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;

    const posHasAvatar = (pos, avatarsList) => {
      let posAsString = JSON.stringify(pos);
      return avatarsList.some((avatarPos) => {
        return JSON.stringify(avatarPos) === posAsString;
      });
    }

    const render = () => {
      let isWhite = true,
          xPos = 0,
          yPos = 0;

      for (let row = 0; row < layout.length; row++) {
        for (let col = 0; col < layout[0].length; col++) {
          ctx.fillStyle = isWhite ? "white" : "black";
          ctx.fillRect(xPos, yPos, tileWidth, tileHeight);
          ctx.fill();

          if (posHasAvatar([row, col], avatars["red"])) {
            ctx.fillStyle = "red";
          } else if (posHasAvatar([row, col], avatars["white"])) {
            ctx.fillStyle = "white";
          }
          ctx.fillRect(xPos + 25, yPos + 25, tileWidth - 50, tileHeight - 50);
          ctx.fill();

          xPos += tileWidth;
          isWhite = !isWhite;
        }
        xPos = 0;
        yPos += tileHeight;
        isWhite = !isWhite;
      }
    }

    render();
  });

  return (
    <BoardCanvas ref={ref} width={canvasWidth} height={canvasHeight}/>
  );
}

export default Board;