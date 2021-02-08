import { useEffect, useRef } from 'react';

const BoardArtist = () => {
  const ref = useRef();

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

  useEffect(()=> {
    let animationFrameId,
        frameCount = 0;

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
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      ctx.fillStyle = '#000000';
      ctx.beginPath();
      ctx.arc(
        canvas.width / 2,
        canvas.height / 2,
        (canvas.width / 2) * Math.abs(Math.cos(frameCount * 0.01)),
        0,
        2 * Math.PI
      );
      ctx.fill();

      animationFrameId = window.requestAnimationFrame(render);
      frameCount ++;
    }

    render();

    return () => {
      window.cancelAnimationFrame(animationFrameId);
    }
  });

  return (
    <canvas ref={ref} />
  );
}

export default BoardArtist;