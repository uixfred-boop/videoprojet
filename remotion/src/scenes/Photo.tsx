import React from 'react';
import {AbsoluteFill, Img, interpolate, OffthreadVideo, useCurrentFrame} from 'remotion';
import {SceneProps} from '../types';
import {Asset, BigNumber, Vignette} from './common';
import {PhoneCard} from './Screen';
import {PhotoLines} from './Draw';

// B-roll photo (C1) : étalonnage ciné, push-in lent, vignette
export const Photo: React.FC<SceneProps> = ({scene}) => {
  const f = useCurrentFrame();
  const dur = scene.to - scene.from;
  const [fx, fy] = scene.focus ?? [0.5, 0.5];
  const scale = interpolate(f, [0, dur], [1.06, 1.06 + (dur / 30) * 0.07]);
  const overlay = !!scene.phoneOverlay;
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img
        src={Asset(scene.src)}
        style={{
          position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${fx * 100}% ${fy * 100}%`,
          transform: `scale(${scale})`, transformOrigin: `${fx * 100}% ${fy * 100}%`,
          filter: overlay ? 'saturate(0.6) brightness(0.45) blur(10px)' : 'saturate(0.72) contrast(1.1) brightness(0.78) sepia(0.18)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(4,7,15,0.15) 0%, rgba(4,7,15,0) 40%, rgba(4,7,15,0.55) 100%)'}} />
      <Vignette strength={0.6} />
      {!overlay && <PhotoLines kind={scene.lines ?? 'frame'} dur={dur} />}
      {scene.num && <BigNumber text={scene.num} y={330} size={260} />}
      {overlay && <PhoneCard src={scene.phoneOverlay} cropCx={596} cropCy={320} cropW={250} f={f} dur={dur} y={170} />}
    </AbsoluteFill>
  );
};
