import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, OffthreadVideo, useCurrentFrame} from 'remotion';
import {getLength, getPointAtLength} from '@remotion/paths';
import {C, FONT} from '../theme';
import {SceneProps} from '../types';
import {Asset, BlueBg, NavyBg, PaperBg} from './common';
import {rateFor} from './Screen';

const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const lockStart = (p: SceneProps, i: number) => (p.lockups[i] ? p.lockups[i].from - p.scene.from : 0);

// ---------- E1 / E2 : ligne qui se dessine, caméra qui suit ----------
const THICK_PATH = 'M -80 260 C 420 200, 900 300, 860 760 C 830 1120, 160 1080, 200 1500 C 240 1900, 900 1820, 880 2300 C 860 2700, 300 2700, 260 3200';
const THIN_PATH = 'M -40 1240 C 260 1080, 520 1500, 760 1180 S 1060 980, 1140 1060';

export const Line: React.FC<SceneProps> = (p) => {
  const f = useCurrentFrame();
  const dur = p.scene.to - p.scene.from;
  const thick = p.scene.variant === 'thick';
  const path = thick ? THICK_PATH : THIN_PATH;
  const L = getLength(path);
  const prog = interpolate(f, [0, dur * (thick ? 0.95 : 0.7)], [0.02, 1], {...clamp, easing: Easing.inOut(Easing.sin)});
  const tip = getPointAtLength(path, L * prog);
  const camY = thick ? Math.max(0, tip.y - 1050) : 0;
  const chips: string[] = p.scene.chips ?? [];
  return (
    <AbsoluteFill>
      <PaperBg />
      <svg width={1080} height={3400} style={{position: 'absolute', left: 0, top: -camY}} viewBox="0 0 1080 3400">
        <path d={path} fill="none" stroke={thick ? C.blue : C.ink} strokeWidth={thick ? 46 : 4} strokeLinecap="butt"
          strokeDasharray={L} strokeDashoffset={L * (1 - prog)} />
        {chips.map((c, i) => {
          const fr = 0.3 + (i * 0.62) / Math.max(1, chips.length);
          const pt = getPointAtLength(path, L * fr);
          const shown = prog >= fr;
          const o = shown ? interpolate(prog - fr, [0, 0.03], [0, 1], clamp) : 0;
          const leftSide = pt.x > 540;
          return (
            <foreignObject key={i} x={leftSide ? pt.x - 560 : pt.x + 40} y={pt.y - 40} width={520} height={90} opacity={o}>
              <div style={{display: 'flex', justifyContent: leftSide ? 'flex-end' : 'flex-start'}}>
                <div style={{fontFamily: FONT.sans, fontWeight: 600, fontSize: 36, color: C.ink, background: '#fff', border: `2px solid rgba(20,17,21,0.12)`, borderRadius: 999, padding: '14px 28px', whiteSpace: 'nowrap', boxShadow: '0 10px 30px rgba(20,17,21,0.08)'}}>{c}</div>
              </div>
            </foreignObject>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

// ---------- E3 : liste de ce qui manquait ----------
export const Strike: React.FC<SceneProps> = ({scene}) => {
  const f = useCurrentFrame();
  const items: {text: string; at: number}[] = scene.items ?? [];
  return (
    <AbsoluteFill>
      <PaperBg />
      <div style={{position: 'absolute', top: 640, left: 150, fontFamily: FONT.sans, fontWeight: 700, fontSize: 30, letterSpacing: '0.14em', textTransform: 'uppercase', color: C.inkSoft}}>What I didn't have</div>
      {items.map((it, i) => {
        const o = interpolate(f - it.at, [0, 5], [0, 1], clamp);
        const x = interpolate(f - it.at, [0, 8], [16, 0], {...clamp, easing: Easing.out(Easing.cubic)});
        return (
          <div key={i} style={{position: 'absolute', top: 730 + i * 150, left: 150, display: 'flex', alignItems: 'center', gap: 30, opacity: o, transform: `translateX(${x}px)`}}>
            <div style={{width: 64, height: 64, borderRadius: 32, border: `3px solid ${C.red}`, display: 'grid', placeItems: 'center', color: C.red, fontFamily: FONT.sans, fontWeight: 600, fontSize: 36}}>✕</div>
            <div style={{fontFamily: FONT.sans, fontWeight: 650 as any, fontSize: 62, letterSpacing: '-0.03em', color: C.ink}}>{it.text}</div>
          </div>
        );
      })}
      <div style={{position: 'absolute', top: 690, left: 150, width: 780, height: 2, background: 'rgba(20,17,21,0.12)'}} />
    </AbsoluteFill>
  );
};

// ---------- E11 : grille de points, un seul s'allume ----------
export const Dots: React.FC<SceneProps> = (p) => {
  const f = useCurrentFrame();
  const dur = p.scene.to - p.scene.from;
  const lightAt = p.lockups[2] ? lockStart(p, 2) : Math.round(dur * 0.65);
  const cols = 9, rows = 11, sp = 100, ox = 540 - ((cols - 1) * sp) / 2, oy = 1150 - ((rows - 1) * sp) / 2;
  const tc = 6, tr = 4;
  const lit = interpolate(f - lightAt, [0, 10], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const dots = [];
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++) {
      const appear = interpolate(f - (r + c) * 0.8, [0, 6], [0, 1], clamp);
      const target = r === tr && c === tc;
      const rad = target ? 9 + 13 * lit : 9;
      const col = target ? (lit > 0.05 ? C.blue : '#CFCAD6') : '#CFCAD6';
      const op = appear * (target ? 1 : 1 - 0.6 * lit);
      dots.push(<circle key={`${r}-${c}`} cx={ox + c * sp} cy={oy + r * sp} r={rad} fill={col} opacity={op} />);
    }
  const tx = ox + tc * sp, ty = oy + tr * sp;
  return (
    <AbsoluteFill>
      <PaperBg />
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
        <circle cx={tx} cy={ty} r={60 * lit} fill={C.halo} opacity={0.35 * lit} />
        {dots}
      </svg>
      <div style={{position: 'absolute', left: tx - 380, top: ty + 50, width: 460, display: 'flex', justifyContent: 'flex-end', opacity: lit}}>
        <div style={{fontFamily: FONT.sans, fontWeight: 700, fontSize: 32, color: '#fff', background: C.blue, borderRadius: 999, padding: '14px 26px', whiteSpace: 'nowrap'}}>{p.scene.label}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- étapes reliées par un trait fin ----------
export const Steps: React.FC<SceneProps> = ({scene}) => {
  const f = useCurrentFrame();
  const nodes: {text: string; at: number}[] = scene.nodes ?? [];
  const ys = [780, 1130, 1480], x = 250;
  return (
    <AbsoluteFill>
      <PaperBg />
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
        {nodes.slice(0, -1).map((n, i) => {
          const nxt = nodes[i + 1];
          const pr = interpolate(f, [n.at + 4, nxt.at], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
          return <line key={i} x1={x} y1={ys[i]} x2={x} y2={ys[i] + (ys[i + 1] - ys[i]) * pr} stroke={C.ink} strokeWidth={3} opacity={0.5} />;
        })}
        {nodes.map((n, i) => {
          const s = interpolate(f - n.at, [0, 8], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.4))});
          return <circle key={i} cx={x} cy={ys[i]} r={22 * s} fill={i === nodes.length - 1 ? C.blue : C.ink} />;
        })}
      </svg>
      {nodes.map((n, i) => {
        const o = interpolate(f - n.at, [0, 6], [0, 1], clamp);
        return (
          <div key={i} style={{position: 'absolute', left: x + 70, top: ys[i], transform: 'translateY(-50%)', opacity: o, fontFamily: i === nodes.length - 1 ? FONT.italic : FONT.sans, fontStyle: i === nodes.length - 1 ? 'italic' : 'normal', fontWeight: 700, fontSize: i === nodes.length - 1 ? 84 : 66, letterSpacing: '-0.03em', color: i === nodes.length - 1 ? C.blue : C.ink}}>
            {n.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------- F2 : photos qui s'empilent sur bleu ----------
const STACK = [
  {src: 'borovsky_house.jpg', x: -70, y: -230, r: -4},
  {src: 'garage_house5.jpg', x: 80, y: -30, r: 3},
  {src: 'plimoth_framing.jpg', x: -50, y: 170, r: -2},
  {src: 'iran_workers.jpg', x: 70, y: 360, r: 4},
];
export const Stack: React.FC<SceneProps> = ({scene}) => {
  const f = useCurrentFrame();
  const dur = scene.to - scene.from;
  const step = Math.max(8, Math.floor((dur * 0.7) / STACK.length));
  return (
    <AbsoluteFill>
      <BlueBg />
      {STACK.map((s, i) => {
        const at = i * step;
        if (f < at) return null;
        const sc = interpolate(f - at, [0, 3], [0.95, 1], clamp);
        const drift = interpolate(f, [0, dur], [0, -20]);
        return (
          <div key={i} style={{position: 'absolute', left: 540 - 330 + s.x, top: 700 - 220 + s.y + drift, width: 660, height: 440, background: '#fff', padding: 12,
            transform: `rotate(${s.r}deg) scale(${sc})`, boxShadow: '0 30px 60px rgba(0,10,60,0.35)'}}>
            <Img src={Asset(s.src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(0.85) contrast(1.05)'}} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------- E10 : détail zoomé + traits de cote ----------
export const Dimension: React.FC<SceneProps> = (p) => {
  const f = useCurrentFrame();
  const dur = p.scene.to - p.scene.from;
  const a1 = lockStart(p, 2), a2 = lockStart(p, 3);
  const k = interpolate(f, [0, dur], [1.6, 1.78]);
  const cw = 920, ch = 1060, cx = 610, cy = 330;
  const o1 = interpolate(f - a1, [0, 8], [0, 1], clamp), o2 = interpolate(f - a2, [0, 8], [0, 1], clamp);
  const w1 = interpolate(f - a1, [0, 12], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const w2 = interpolate(f - a2, [0, 14], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const lab: React.CSSProperties = {position: 'absolute', fontFamily: FONT.sans, fontWeight: 700, fontSize: 34, color: '#fff', letterSpacing: '0.02em'};
  return (
    <AbsoluteFill>
      <NavyBg />
      <div style={{position: 'absolute', left: 80, top: 190, width: cw, height: ch, borderRadius: 26, overflow: 'hidden', background: '#fff', boxShadow: '0 0 120px 10px rgba(40,90,255,0.3)'}}>
        <OffthreadVideo src={Asset(p.scene.src)} muted playbackRate={rateFor(p.scene.src, dur)}
          style={{position: 'absolute', maxWidth: 'none', width: 1196 * k, height: 640 * k, left: cw / 2 - cx * k, top: ch / 2 - cy * k}} />
      </div>
      {/* cote horizontale « 3 px » */}
      <div style={{position: 'absolute', left: 300, top: 470, width: 300 * w1, height: 3, background: C.halo, opacity: o1}} />
      <div style={{position: 'absolute', left: 300, top: 452, width: 3, height: 40, background: C.halo, opacity: o1}} />
      <div style={{position: 'absolute', left: 300 + 300 * w1, top: 452, width: 3, height: 40, background: C.halo, opacity: o1}} />
      <div style={{...lab, left: 330, top: 395, opacity: o1, background: C.blue, padding: '6px 16px', borderRadius: 8}}>3 px</div>
      {/* barre de timing « 0.1 s » */}
      <div style={{position: 'absolute', left: 180, top: 1120, width: 720, height: 3, background: 'rgba(255,255,255,0.25)', opacity: o2}} />
      <div style={{position: 'absolute', left: 180, top: 1112, width: 720 * w2 * 0.82, height: 18, background: C.blue, borderRadius: 9, opacity: o2}} />
      <div style={{...lab, left: 180 + 720 * 0.82 - 70, top: 1150, opacity: o2}}>−0.1 s</div>
    </AbsoluteFill>
  );
};

// ---------- deux lignes fines qui convergent ----------
export const Converge: React.FC<SceneProps> = ({scene}) => {
  const f = useCurrentFrame();
  const dur = scene.to - scene.from;
  const pr = interpolate(f, [4, dur * 0.85], [0, 1], {...clamp, easing: Easing.inOut(Easing.sin)});
  const A = 'M 250 330 C 250 700, 540 760, 540 1080 L 540 1300';
  const B = 'M 830 330 C 830 700, 540 760, 540 1080 L 540 1300';
  const la = getLength(A), lb = getLength(B);
  const lab = (t: string, x: number, c: string, it = false): React.ReactNode => (
    <div style={{position: 'absolute', top: 250, left: x - 200, width: 400, textAlign: 'center', fontFamily: it ? FONT.italic : FONT.sans, fontStyle: it ? 'italic' : 'normal', fontWeight: 700, fontSize: 52, color: c, opacity: interpolate(f, [0, 8], [0, 1], clamp)}}>{t}</div>
  );
  return (
    <AbsoluteFill>
      <PaperBg />
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
        <path d={A} fill="none" stroke={C.ink} strokeWidth={4} strokeDasharray={la} strokeDashoffset={la * (1 - pr)} />
        <path d={B} fill="none" stroke={C.blue} strokeWidth={4} strokeDasharray={lb} strokeDashoffset={lb * (1 - pr)} />
        <circle cx={540} cy={1080} r={14 * interpolate(pr, [0.62, 0.7], [0, 1], clamp)} fill={C.blue} />
      </svg>
      {lab('strategy', 250, C.ink)}
      {lab('design', 830, C.blue, true)}
    </AbsoluteFill>
  );
};
