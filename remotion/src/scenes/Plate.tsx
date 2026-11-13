import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C} from '../theme';
import {SceneProps} from '../types';
import {BigNumber, BlueBg, NavyBg, PaperBg} from './common';

export const Plate: React.FC<SceneProps> = ({scene}) => {
  const bg = scene.bg;
  const num: string | undefined = scene.num;
  return (
    <AbsoluteFill>
      {bg === 'blue' ? <BlueBg /> : bg === 'paper' ? <PaperBg /> : <NavyBg />}
      {num && num.length === 1 && <BigNumber text={num} y={760} size={620} color={bg === 'paper' ? C.blue : bg === 'navy' ? '#4E7BFF' : '#FFFFFF'} />}
      {num && num.length > 1 && <BigNumber text={num} y={640} size={300} color={bg === 'paper' ? C.blue : '#FFFFFF'} />}
    </AbsoluteFill>
  );
};
