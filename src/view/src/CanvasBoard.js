import styled from "styled-components";
import { useEffect, useRef } from "react";

const BoardCanvas = styled.canvas`
  /* border: 1px solid black; */
`;

const CanvasBoard = (props) => {
  const { tileSize, gameType, layout, avatars} = props;

  const ref = useRef();

  const angle = 2 * Math.PI / 6;

  const canvasWidth = layout.length * tileSize;
  const canvasHeight = layout[0].length * tileSize;

  const posInList = (pos, posList) => {
    let posAsString = JSON.stringify(pos);
    return posList.some((avatarPos) => {
      return JSON.stringify(avatarPos) === posAsString;
    });
  }

  const tileHasAvatar = (pos) => {
    for (const [color, playerAvatars] of Object.entries(avatars)) {
      if (posInList(pos, playerAvatars)) {
        return color;
      }
    }
    return false;
  }

  useEffect(() => {
    const canvas = ref.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)

    const { width, height } = canvas.getBoundingClientRect();

    if (canvas.width !== width || canvas.height !== height) {
      const { devicePixelRatio:ratio=1 } = window;
      canvas.width = width*ratio;
      canvas.height = height*ratio;
      ctx.scale(ratio, ratio);
    }

    const drawSquare = (x, y, size, color) => {
      ctx.fillStyle = color;
      ctx.fillRect(x, y, size, size);
    }

    const drawHexagon = (x, y, r, color) => {
      ctx.fillStyle = color;
      ctx.strokeStyle = "gray";
      ctx.beginPath();
      for (let i = 0; i < 6; i++) {
        ctx.lineTo(x + r * Math.cos(angle * i), y + r * Math.sin(angle * i));
      }
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }

    const drawCircle = (x, y, r, color) => {
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, r, 0 , 2 * Math.PI);
      ctx.fill();
    }

    const drawFish = (x, y, size, numFishes) => {
      let fishSize = size / 3;
      ctx.fillStyle = "gray";
      ctx.textAlign = "center";
      ctx.font = `${fishSize}px monospace`;
      ctx.fillText(numFishes, x, y + (fishSize / 3));
    }

    const render = () => {
      let isWhite = true,
          avatarSize = tileSize / 3,
          xPos = gameType === "checker" ? 0 : (tileSize / 2),
          yPos = gameType === "checker" ? 0 : (tileSize / 2) * Math.sin(angle);

      for (let row = 0; row < layout.length; row++) {
        for (let col = 0; col < layout[0].length; col++) {
          let tileColor = isWhite ? "white" : "black";
          let hasAvatar = tileHasAvatar([row, col]);
          switch (gameType) {
            case "checker":
              drawSquare(xPos, yPos, tileSize, tileColor);
              if (hasAvatar) {
                drawCircle(
                  xPos + tileSize / 2, 
                  yPos + tileSize / 2,
                  avatarSize, 
                  hasAvatar
                );
              }
              xPos += tileSize;
              break;
            case "fish":
              if (layout[row][col] !== 0) {
                drawHexagon(xPos, yPos, tileSize / 2, tileColor);
                if (hasAvatar) {
                  drawCircle(
                    xPos, 
                    yPos,
                    avatarSize, 
                    hasAvatar
                  );
                } else {
                  drawFish(xPos, yPos, tileSize, layout[row][col]);
                }
              }
              xPos += (tileSize / 2) * (1 + Math.cos(angle));
              yPos += (-1) ** col * (tileSize / 2) * Math.sin(angle);
              break;
            default:
              console.log("Unsupported game type")
          }
          
          isWhite = !isWhite;
        }
        switch (gameType) {
          case "checker":
            xPos = 0;
            yPos += tileSize;
            break;
          case "fish":
            xPos = (tileSize / 2)
            yPos += tileSize * Math.sin(angle);
            if (layout.length % 2 !== 0)
              yPos -= (tileSize / 2) * Math.sin(angle);
            break;
          default:
            console.log("Unsupported game type")
        }
        isWhite = !isWhite;
      }
    }

    render();
  });

  return (
    <BoardCanvas ref={ref} width={canvasWidth} height={canvasHeight}/>
  );
}

export default CanvasBoard;