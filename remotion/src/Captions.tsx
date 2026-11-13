import React from 'react';
import {AbsoluteFill, Easing, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {C, FONT} from './theme';
import {Lockup, Scene, ShortData, Word} from './types';

type Place = {y: number; dark: boolean; K: number; sat: number; plain: number; aroll: boolean; accentOnPaper: boolean};

// Où et comment poser le texte selon la scène (skill §4.10)
export const placement = (s: Scene): Place => {
  const base = {dark: false, aroll: false, accentOnPaper: false};
  switch (s.type) {
    case 'face':
      return {...base, y: 1452, K: 112, sat: 38, plain: 52, aroll: true};
    case 'plate': {
      const dark = s.bg === 'paper';
      return {...base, y: s.num ? 1090 : 960, K: 168, sat: 44, plain: 66, dark, accentOnPaper: dark};
    }
    case 'photo':
      return {...base, y: s.phoneOverlay ? 1470 : s.num ? 1180 : 1150, K: 150, sat: 42, plain: 60, aroll: true};
    case 'screen':
      return {...base, y: s.phone || s.morph ? 1452 : 1400, K: 120, sat: 40, plain: 54, aroll: true};
    case 'reels':
      return {...base, y: 980, K: 150, sat: 42, plain: 58};
    case 'illustration':
      return {...base, y: 400, K: 150, sat: 42, plain: 58};
    case 'line':
      return {...base, y: s.chips ? 380 : 980, K: 140, sat: 42, plain: 60, dark: true, accentOnPaper: true};
    case 'dimension':
      return {...base, y: 1500, K: 120, sat: 40, plain: 54, aroll: true};
    case 'converge':
      return {...base, y: 1520, K: 130, sat: 42, plain: 58, dark: true, accentOnPaper: true};
    case 'dots':
    case 'steps':
      return {...base, y: 360, K: 120, sat: 40, plain: 56, dark: true, accentOnPaper: true};
    case 'stack':
      return {...base, y: 1560, K: 130, sat: 42, plain: 58};
    default:
      return {...base, y: 960, K: 140, sat: 42, plain: 58};
  }
};

const FACTOR: Record<string, number> = {b: 0.6, i: 0.52, s: 0.4, x: 0.46, m: 0.56, g: 0.52, base: 0.52};
const keyFont = (style: string, K: number) => {
  switch (style) {
    case 'b':
      return {fontFamily: FONT.sans, fontWeight: 900, fontSize: K, letterSpacing: '-0.045em'};
    case 's':
      return {fontFamily: FONT.serif, fontWeight: 400, fontSize: K * 1.12, letterSpacing: '-0.025em'};
    case 'x':
      return {fontFamily: FONT.italic, fontStyle: 'italic', fontWeight: 700, fontSize: K * 0.74, letterSpacing: '-0.01em'};
    case 'm':
      return {fontFamily: FONT.sans, fontWeight: 800, fontSize: K * 0.8, letterSpacing: '-0.035em'};
    default: // i, g
      return {fontFamily: FONT.italic, fontStyle: 'italic', fontWeight: 700, fontSize: K * 0.92, letterSpacing: '-0.01em'};
  }
};

const WordSpan: React.FC<{w: Word; f: number; aroll: boolean; color: string; style?: React.CSSProperties}> = ({w, f, aroll, color, style}) => {
  const local = f - w.at;
  const o = aroll ? interpolate(local, [0, 5], [0.4, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.quad)}) : 1;
  return <span style={{color, opacity: o * (w.style === 'g' ? 0.45 : 1), ...style}}>{w.text}</span>;
};

const join = (els: React.ReactNode[]) => els.flatMap((e, i) => (i ? [' ', e] : [e]));

export const LockupView: React.FC<{l: Lockup; s: Scene}> = ({l, s}) => {
  const f = useCurrentFrame();
  const P = placement(s);
  const words = l.words.filter((w) => w.at <= f);
  if (!words.length) return null;
  const fg = P.dark ? C.ink : '#FFFFFF';
  const keyIdx = l.words.map((w, i) => (w.style !== 'base' ? i : -1)).filter((i) => i >= 0);
  const halo = s.type === 'line' || s.type === 'converge' ? {textShadow: `0 0 22px ${C.paper}, 0 0 10px ${C.paper}, 0 0 4px ${C.paper}`} : {};
  const satStyle: React.CSSProperties = {fontFamily: FONT.sans, fontWeight: 600, fontSize: P.sat, letterSpacing: '-0.02em', lineHeight: 1.12, ...halo};

  let body: React.ReactNode;
  if (!keyIdx.length) {
    const len = l.words.map((w) => w.text).join(' ').length;
    const size = Math.min(P.plain, 940 / (len * 0.52));
    body = (
      <div style={{...satStyle, fontSize: size, textAlign: 'center', maxWidth: 940, fontWeight: 650 as any}}>
        {join(words.map((w, i) => <WordSpan key={i} w={w} f={f} aroll={P.aroll} color={fg} />))}
      </div>
    );
  } else {
    const k0 = keyIdx[0], k1 = keyIdx[keyIdx.length - 1];
    const pre = l.words.slice(0, k0), key = l.words.slice(k0, k1 + 1), post = l.words.slice(k1 + 1);
    const ks = key.find((w) => w.style !== 'base')!.style;
    const keyText = key.map((w) => w.text).join(' ');
    let K = P.K;
    const est = keyText.length * K * (FACTOR[ks] ?? 0.52) * (ks === 's' ? 1.12 : ks === 'x' ? 0.74 : ks === 'm' ? 0.8 : ks === 'b' ? 1 : 0.92);
    if (est > 900) K = (K * 900) / est;
    const kf = keyFont(ks, K);
    const vis = (arr: Word[]) => arr.filter((w) => w.at <= f);
    let keyColor = fg;
    if (P.accentOnPaper && (ks === 'b' || ks === 'i')) keyColor = C.blue;
    if (ks === 'x') keyColor = '#FFFFFF';
    const keyStart = key[0].at;
    const wipe = interpolate(f - keyStart, [0, 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.2, 0.8, 0.2, 1)});
    const onBlue = s.type === 'plate' && s.bg === 'blue';
    const markerBg = onBlue ? C.paper : C.blue;
    const markerFg = onBlue ? C.blue : '#FFFFFF';
    const keyEls = vis(key).map((w, i) => (
      <WordSpan key={i} w={w} f={f} aroll={P.aroll && ks !== 'x'} color={ks === 'm' && f >= keyStart ? markerFg : w.style === 'base' ? fg : keyColor} style={w.style === 'base' ? {...satStyle} : {}} />
    ));
    const hasPre = vis(pre).length > 0, hasPost = vis(post).length > 0;
    body = (
      <div style={{display: 'inline-flex', flexDirection: 'column', alignItems: 'center', maxWidth: 960}}>
        {hasPre && (
          <div style={{...satStyle, alignSelf: post.length ? 'flex-start' : 'center', marginLeft: post.length ? 8 : 0, marginBottom: ks === 'x' || ks === 'm' ? 10 : 2, maxWidth: 940}}>
            {join(vis(pre).map((w, i) => <WordSpan key={i} w={w} f={f} aroll={P.aroll} color={fg} />))}
          </div>
        )}
        <div style={{position: 'relative', lineHeight: 0.95, whiteSpace: 'nowrap', ...kf, ...halo, padding: ks === 'x' || ks === 'm' ? '2px 22px 14px' : 0}}>
          {(ks === 'x' || ks === 'm') && (
            <div style={{position: 'absolute', inset: 0, background: ks === 'x' ? C.blue : markerBg, clipPath: `inset(0 ${100 - wipe * 100}% 0 0)`}} />
          )}
          <span style={{position: 'relative'}}>{join(keyEls)}</span>
        </div>
        {hasPost && (
          <div style={{...satStyle, alignSelf: pre.length ? 'flex-end' : 'center', marginRight: pre.length ? 8 : 0, marginTop: ks === 'x' || ks === 'm' ? 10 : 4, maxWidth: 940, textAlign: 'right'}}>
            {join(vis(post).map((w, i) => <WordSpan key={i} w={w} f={f} aroll={P.aroll} color={fg} />))}
          </div>
        )}
      </div>
    );
  }
  const qColor = P.dark ? C.blue : s.type === 'plate' && s.bg === 'blue' ? 'rgba(255,255,255,0.55)' : C.halo;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', top: P.y, left: 50, right: 50, transform: 'translateY(-50%)', display: 'flex', justifyContent: 'center'}}>
        <div style={{position: 'relative'}}>
          {l.quoted && (
            <div style={{position: 'absolute', left: -70, top: -130, fontFamily: FONT.serif, fontSize: 260, lineHeight: 1, color: qColor}}>“</div>
          )}
          {body}
          {l.quoted && words.length === l.words.length && (
            <div style={{position: 'absolute', right: -78, bottom: -168, fontFamily: FONT.serif, fontSize: 260, lineHeight: 1, color: qColor}}>”</div>
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC<{data: ShortData}> = ({data}) => (
  <>
    {data.lockups
      .filter((l) => !l.hidden)
      .map((l, i) => (
        <Sequence key={i} from={l.from} durationInFrames={Math.max(1, l.to - l.from)} layout="none">
          <LockupView l={l} s={data.scenes[l.scene]} />
        </Sequence>
      ))}
  </>
);
