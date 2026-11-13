import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile} from 'remotion';
import {Captions} from './Captions';
import {Grain} from './scenes/common';
import {Face} from './scenes/Face';
import {Plate} from './scenes/Plate';
import {Photo} from './scenes/Photo';
import {Screen} from './scenes/Screen';
import {Converge, Dimension, Dots, Line, Stack, Steps, Strike} from './scenes/Diagrams';
import {Cta, Illustration, Reels} from './scenes/Graphics';
import {Draw} from './scenes/Draw';
import {SceneProps, ShortData} from './types';

const SCENES: Record<string, React.FC<SceneProps>> = {
  face: Face, plate: Plate, photo: Photo, screen: Screen, line: Line, strike: Strike, dots: Dots,
  steps: Steps, stack: Stack, dimension: Dimension, converge: Converge, reels: Reels, illustration: Illustration, draw: Draw,
};
const WHOOSH = new Set(['screen', 'reels', 'illustration', 'line', 'stack', 'dimension', 'converge', 'dots', 'steps', 'draw', 'photo']);

export type ShortProps = {data: ShortData; voiceSrc: string};

export const Short: React.FC<ShortProps> = ({data, voiceSrc}) => {
  const fps = data.fps;
  const sfx: {src: string; at: number; vol: number}[] = [];
  data.scenes.forEach((s, i) => {
    const prev = data.scenes[i - 1];
    if (i > 0 && WHOOSH.has(s.type) && prev.type !== s.type) sfx.push({src: 'whoosh.wav', at: s.from - 8, vol: 0.22});
    if (s.type === 'strike') (s.items ?? []).forEach((it: any) => it.at > 0 && sfx.push({src: 'click.wav', at: s.from + it.at, vol: 0.25}));
    if (s.type === 'steps') (s.nodes ?? []).forEach((n: any) => sfx.push({src: 'click.wav', at: s.from + n.at, vol: 0.25}));
    if (s.type === 'stack') for (let k = 0; k < 4; k++) sfx.push({src: 'pop.wav', at: s.from + k * Math.max(8, Math.floor(((s.to - s.from) * 0.7) / 4)), vol: 0.3});
  });
  sfx.push({src: 'riser.wav', at: data.cta.from - 44, vol: 0.18});
  const total = data.durationInFrames;
  return (
    <AbsoluteFill style={{background: '#04070F'}}>
      {data.scenes.map((s) => {
        const Comp = SCENES[s.type];
        const lockups = data.lockups.filter((l) => l.scene === s.idx);
        return (
          <Sequence key={s.idx} from={s.from} durationInFrames={Math.max(1, s.to - s.from)}>
            <Comp scene={s} data={data} lockups={lockups} />
          </Sequence>
        );
      })}
      <Sequence from={data.cta.from} durationInFrames={data.cta.to - data.cta.from}>
        <Cta word={data.cta.word} line={data.cta.line} dur={data.cta.to - data.cta.from} />
      </Sequence>
      <Captions data={data} />
      <Grain />
      {/* voix (séparée de la musique d'origine) */}
      {data.voice.map((v, i) => (
        <Sequence key={`v${i}`} from={v.from} durationInFrames={Math.round((v.src1 - v.src0) * fps)}>
          <Audio src={staticFile(voiceSrc)} startFrom={Math.round(v.src0 * fps)} endAt={Math.round(v.src1 * fps)}
            volume={(f) => interpolate(f, [0, 2, (v.src1 - v.src0) * fps - 3, (v.src1 - v.src0) * fps], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
        </Sequence>
      ))}
      {/* beat rap instrumental, légèrement effacé quand la voix parle (vad), remonté sur le CTA */}
      <Audio src={staticFile('audio/beat.wav')}
        volume={(f) => {
          const vad: string = (data as any).vad ?? '';
          let on = 0;
          for (let k = f - 6; k <= f + 6; k++) if (vad[k] === '1') on++;
          const base = f >= data.cta.from ? interpolate(f, [data.cta.from, data.cta.from + 8], [0.2, 0.5], {extrapolateRight: 'clamp'}) : 0.27 - 0.08 * (on / 13);
          return base * interpolate(f, [0, 3, total - 16, total], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        }} />
      {sfx.map((s, i) => (
        <Sequence key={`s${i}`} from={Math.max(0, s.at)}>
          <Audio src={staticFile(`audio/${s.src}`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
