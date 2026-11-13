import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {SceneProps} from '../types';
import {BigNumber, BlueBg, NavyBg, PaperBg} from './common';

// Fil vertical : la ligne descend jusqu'au texte, s'interrompt, puis repart vers le bas (principe « ligne + texte »)
export const Thread: React.FC<{y: number; gap?: number; dur: number; color: string; top?: boolean}> = ({y, gap = 210, dur, color, top = true}) => {
  const f = useCurrentFrame();
  const e = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const, easing: Easing.inOut(Easing.cubic)};
  const pTop = interpolate(f, [0, 12], [0, 1], e);
  const pBot = interpolate(f, [Math.max(8, dur * 0.45), Math.max(20, dur * 0.95)], [0, 1], e);
  const yTop = y - gap, yBot = y + gap;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
      {top && <line x1={540} y1={0} x2={540} y2={yTop * pTop} stroke={color} strokeWidth={3} />}
      {top && pTop > 0.98 && <circle cx={540} cy={yTop} r={7} fill={color} />}
      {pBot > 0 && <circle cx={540} cy={yBot} r={7} fill={color} />}
      <line x1={540} y1={yBot} x2={540} y2={yBot + (1920 - yBot) * pBot} stroke={color} strokeWidth={3} />
    </svg>
  );
};

export const Plate: React.FC<SceneProps> = ({scene}) => {
  const bg = scene.bg;
  const num: string | undefined = scene.num;
  const dur = scene.to - scene.from;
  const lineColor = bg === 'paper' ? 'rgba(20,17,21,0.55)' : bg === 'blue' ? 'rgba(255,255,255,0.7)' : C.halo;
  return (
    <AbsoluteFill>
      {bg === 'blue' ? <BlueBg /> : bg === 'paper' ? <PaperBg /> : <NavyBg />}
      <Thread y={num ? 1090 : 960} dur={dur} color={lineColor} top={!num} gap={num ? 190 : 230} />
      {num && num.length === 1 && <BigNumber text={num} y={760} size={620} color={bg === 'paper' ? C.blue : bg === 'navy' ? '#4E7BFF' : '#FFFFFF'} />}
      {num && num.length > 1 && <BigNumber text={num} y={640} size={300} color={bg === 'paper' ? C.blue : '#FFFFFF'} />}
    </AbsoluteFill>
  );
};
