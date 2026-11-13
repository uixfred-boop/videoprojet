import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {C} from '../theme';
import {SceneProps} from '../types';
import {BlueBg, NavyBg, PaperBg} from './common';

// Illustrations au trait (viewBox 600x600), dessinées trait après trait. accent = tracé en bleu/halo.
type Stroke = {d: string; accent?: boolean};
const ICONS: Record<string, Stroke[]> = {
  twins: [
    {d: 'M 250 200 A 60 60 0 1 1 130 200 A 60 60 0 1 1 250 200'},
    {d: 'M 80 440 C 80 330, 300 330, 300 440'},
    {d: 'M 470 200 A 60 60 0 1 1 350 200 A 60 60 0 1 1 470 200'},
    {d: 'M 300 440 C 300 330, 520 330, 520 440'},
    {d: 'M 250 505 L 350 505 M 250 535 L 350 535', accent: true},
  ],
  target: [
    {d: 'M 540 300 A 240 240 0 1 1 60 300 A 240 240 0 1 1 540 300'},
    {d: 'M 460 300 A 160 160 0 1 1 140 300 A 160 160 0 1 1 460 300'},
    {d: 'M 380 300 A 80 80 0 1 1 220 300 A 80 80 0 1 1 380 300'},
    {d: 'M 585 15 L 306 294', accent: true},
    {d: 'M 585 15 L 530 20 M 585 15 L 580 70', accent: true},
  ],
  bubble: [
    {d: 'M 130 130 H 470 Q 520 130 520 180 V 360 Q 520 410 470 410 H 270 L 180 485 L 200 410 H 130 Q 80 410 80 360 V 180 Q 80 130 130 130 Z'},
    {d: 'M 230 270 A 16 16 0 1 1 198 270 A 16 16 0 1 1 230 270', accent: true},
    {d: 'M 316 270 A 16 16 0 1 1 284 270 A 16 16 0 1 1 316 270', accent: true},
    {d: 'M 402 270 A 16 16 0 1 1 370 270 A 16 16 0 1 1 402 270', accent: true},
  ],
};

export const LineArt: React.FC<{icon: string; dur: number; color: string; accent: string; cx?: number; cy?: number; size?: number}> = ({icon, dur, color, accent, cx = 540, cy = 760, size = 640}) => {
  const f = useCurrentFrame();
  const strokes = ICONS[icon] ?? [];
  const total = Math.min(Math.max(24, dur * 0.6), 54);
  const per = total / Math.max(1, strokes.length);
  const push = interpolate(f, [0, dur], [1, 1.06]);
  return (
    <svg width={size} height={size} viewBox="-20 -20 640 640" style={{position: 'absolute', left: cx - size / 2, top: cy - size / 2, transform: `scale(${push})`, overflow: 'visible'}}>
      {strokes.map((s, i) => {
        const p = interpolate(f, [i * per, (i + 1) * per + 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
        return <path key={i} d={s.d} fill="none" stroke={s.accent ? accent : color} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />;
      })}
    </svg>
  );
};

export const Draw: React.FC<SceneProps> = ({scene}) => {
  const bg = scene.bg ?? 'navy';
  const dur = scene.to - scene.from;
  const color = bg === 'paper' ? C.ink : '#FFFFFF';
  const accent = bg === 'paper' ? C.blue : bg === 'blue' ? C.paper : C.halo;
  return (
    <AbsoluteFill>
      {bg === 'blue' ? <BlueBg /> : bg === 'paper' ? <PaperBg /> : <NavyBg />}
      <LineArt icon={scene.icon} dur={dur} color={color} accent={accent} />
    </AbsoluteFill>
  );
};

// Lignes tracées par-dessus un B-roll : cadre fin, ou fourche (décision)
export const PhotoLines: React.FC<{kind: string; dur: number}> = ({kind, dur}) => {
  const f = useCurrentFrame();
  const e = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const, easing: Easing.inOut(Easing.cubic)};
  if (kind === 'fork') {
    const p1 = interpolate(f, [0, 16], [0, 1], e), p2 = interpolate(f, [14, 34], [0, 1], e);
    const stem = 'M 540 1920 L 540 1180', a = 'M 540 1180 C 540 980, 300 900, 250 640', b = 'M 540 1180 C 540 980, 780 900, 830 640';
    return (
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
        <path d={stem} stroke="#fff" strokeWidth={5} fill="none" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p1} />
        <path d={a} stroke="rgba(255,255,255,0.6)" strokeWidth={5} fill="none" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p2} />
        <path d={b} stroke={C.halo} strokeWidth={5} fill="none" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p2} />
        {p2 > 0.98 && <circle cx={250} cy={640} r={12} fill="rgba(255,255,255,0.8)" />}
        {p2 > 0.98 && <circle cx={830} cy={640} r={12} fill={C.halo} />}
      </svg>
    );
  }
  // cadre fin qui se trace dans le sens horaire
  const p = interpolate(f, [0, 22], [0, 1], e);
  const m = 64, w = 1080 - 2 * m, h = 1920 - 2 * m;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
      <rect x={m} y={m} width={w} height={h} fill="none" stroke="rgba(255,255,255,0.75)" strokeWidth={2.5} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} />
    </svg>
  );
};
