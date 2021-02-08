import styled from 'styled-components';
import { useEffect, useRef } from 'react';

const BoardCanvas = styled.canvas`
  width: 750px;
  height: 750px;
  border: 1px solid black;
  background-color: lightblue;
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
  const { layout} = props;

  const ref = useRef();

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

    const render = () => {
      ctx.fillStyle = "gray";
      let xPos = 0,
          yPos = 0,
          xOffset = 85,
          yOffset = 85;

      for (let row = 0; row < layout.length; row++) {
        for (let col = 0; col < layout[0].length; col++) {
          ctx.beginPath();
          ctx.fillRect(xPos, yPos, xOffset, yOffset);
          ctx.strokeRect(xPos, yPos, xOffset, yOffset);
          ctx.fill();
          xPos += xOffset;
        }
        xPos = 0;
        yPos += yOffset;
      }
    }

    render();
  });

  return (
    <BoardCanvas ref={ref} />
  );
}

export default Board;