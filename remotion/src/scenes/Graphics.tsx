import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, useCurrentFrame} from 'remotion';
import {C, FONT} from '../theme';
import {SceneProps} from '../types';
import {Asset, NavyBg} from './common';

const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

// ---------- G4 : cartes de Reels flottantes ----------
const CARDS = [
  {x: 60, y: 170, s: 1, views: '635K', d: 1.0},
  {x: 420, y: 90, s: 0.8, views: '331K', d: 0.6},
  {x: 760, y: 210, s: 0.95, views: '1.2M', d: 0.9},
  {x: -60, y: 1260, s: 0.9, views: '325K', d: 0.8},
  {x: 330, y: 1330, s: 1.05, views: '2.4M', d: 1.1},
  {x: 740, y: 1250, s: 0.85, views: '600K', d: 0.7},
  {x: 900, y: 640, s: 0.7, views: '88K', d: 0.5},
  {x: -110, y: 700, s: 0.7, views: '412K', d: 0.5},
];
export const Reels: React.FC<SceneProps> = ({scene}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <NavyBg />
      {CARDS.map((c, i) => {
        const o = 1;
        const dy = -f * 0.9 * c.d;
        const blur = c.s < 0.8 ? 3 : 0;
        return (
          <div key={i} style={{position: 'absolute', left: c.x, top: c.y + dy, width: 250 * c.s, height: 444 * c.s, borderRadius: 22 * c.s, overflow: 'hidden', opacity: o * (c.s < 0.8 ? 0.55 : 0.9),
            filter: `blur(${blur}px)`, boxShadow: '0 30px 60px rgba(0,0,0,0.5)', border: '1px solid rgba(255,255,255,0.08)'}}>
            <Img src={Asset(`thumb${(i % 8) + 1}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(0.7) brightness(0.75)'}} />
            <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75) 100%)'}} />
            <div style={{position: 'absolute', left: 16 * c.s, bottom: 16 * c.s, fontFamily: FONT.sans, fontWeight: 800, fontSize: 30 * c.s, color: '#fff', letterSpacing: '-0.02em'}}>▶ {c.views}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------- D3 : personnage plat, la tête s'ouvre ----------
export const Illustration: React.FC<SceneProps> = ({scene}) => {
  const f = useCurrentFrame();
  const dur = scene.to - scene.from;
  const open = interpolate(f, [6, 26], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const push = interpolate(f, [0, dur], [1, 1.07]);
  const glow = interpolate(f, [14, 40], [0, 1], clamp);
  return (
    <AbsoluteFill style={{background: `linear-gradient(160deg, ${C.blue} 0%, #0A2A9E 35%, ${C.navy} 70%, ${C.navyDeep} 100%)`, overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `scale(${push})`, transformOrigin: '50% 75%'}}>
        <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
          <defs>
            <radialGradient id="g" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.95} />
              <stop offset="35%" stopColor={C.halo} stopOpacity={0.6} />
              <stop offset="100%" stopColor={C.halo} stopOpacity={0} />
            </radialGradient>
          </defs>
          {/* lueur qui sort de la tête */}
          <ellipse cx={540} cy={880} rx={360 * glow} ry={300 * glow} fill="url(#g)" />
          {/* épaules et cou */}
          <path d="M 120 1920 L 170 1560 Q 200 1420 380 1390 L 460 1330 L 460 1250 L 620 1250 L 620 1330 L 700 1390 Q 880 1420 910 1560 L 960 1920 Z" fill="#05060A" />
          {/* tête (bas) */}
          <path d="M 330 1000 L 750 1000 L 770 1240 Q 690 1300 540 1300 Q 390 1300 310 1240 Z" fill="#05060A" />
          {/* yeux */}
          <ellipse cx={455} cy={1100} rx={52} ry={26} fill="#fff" />
          <ellipse cx={630} cy={1100} rx={52} ry={26} fill="#fff" />
          <circle cx={466} cy={1100} r={15} fill="#05060A" />
          <circle cx={641} cy={1100} r={15} fill="#05060A" />
          {/* couvercle du crâne : charnière à gauche */}
          <g transform={`rotate(${-38 * open} 330 1000)`}>
            <path d="M 330 1000 Q 330 800 540 790 Q 750 800 750 1000 Z" fill="#05060A" />
          </g>
        </svg>
      </div>
    </AbsoluteFill>
  );
};

// ---------- CTA final ----------
export const Cta: React.FC<{word: string; line: string; dur: number}> = ({word, line, dur}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 5], [0, 1], clamp);
  const out = interpolate(f, [dur - 14, dur], [1, 0], clamp);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{opacity: out, background: `radial-gradient(110% 70% at 50% 45%, #1A5CFF 0%, ${C.blue} 55%, #0036D6 100%)`}}>
        <div style={{position: 'absolute', top: 960, left: 0, right: 0, transform: 'translateY(-50%)', textAlign: 'center', color: '#fff', opacity: o}}>
          <div style={{fontFamily: FONT.sans, fontWeight: 600, fontSize: 52, letterSpacing: '-0.02em'}}>Comment</div>
          <div style={{fontFamily: FONT.serif, fontSize: 190, lineHeight: 1, letterSpacing: '-0.02em', marginTop: 6}}>“{word}”</div>
          <div style={{fontFamily: FONT.sans, fontWeight: 500, fontSize: 38, marginTop: 22, opacity: 0.9}}>{line}</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
