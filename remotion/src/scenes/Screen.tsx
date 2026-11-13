import React from 'react';
import {AbsoluteFill, Easing, interpolate, OffthreadVideo, useCurrentFrame} from 'remotion';
import {SceneProps} from '../types';
import {Asset, NavyBg} from './common';

// Captures du site (rush), 1196x640, extraites sans le cadre d'origine
export const CLIP_DUR: Record<string, number> = {
  'scr_grid.mp4': 5.1, 'scr_site.mp4': 5.3, 'scr_hero.mp4': 5.4, 'scr_mobile.mp4': 5.2, 'scr_editor.mp4': 6.8, 'scr_editor2.mp4': 4.2,
};
const SW = 1196, SH = 640;
export const CLIP_START: Record<string, number> = {'scr_mobile.mp4': 0.6, 'scr_hero.mp4': 0.2, 'scr_editor.mp4': 0.3};
export const rateFor = (src: string, frames: number) => Math.min(1, (((CLIP_DUR[src] ?? 5) - (CLIP_START[src] ?? 0)) * 30) / Math.max(1, frames) * 0.97);

const PHONE_FRAME: React.CSSProperties = {
  position: 'absolute', overflow: 'hidden', background: '#fff',
  boxShadow: '0 0 0 12px #0B0D14, 0 0 0 14px rgba(255,255,255,0.12), 0 0 140px 20px rgba(40,90,255,0.35), 0 50px 100px rgba(0,0,0,0.6)',
};

export const PhoneCard: React.FC<{src: string; cropCx: number; cropCy: number; cropW: number; f: number; dur: number; y?: number}> = ({src, cropCx, cropCy, cropW, f, dur, y = 230}) => {
  const w = 500, h = 1000;
  const k = (w / cropW) * interpolate(f, [0, dur], [1, 1.04]);
  return (
    <div style={{...PHONE_FRAME, left: (1080 - w) / 2, top: y, width: w, height: h, borderRadius: 60}}>
      <OffthreadVideo src={Asset(src)} muted playbackRate={rateFor(src, dur)} startFrom={Math.round((CLIP_START[src] ?? 0) * 30)}
        style={{position: 'absolute', maxWidth: 'none', width: SW * k, height: SH * k, left: w / 2 - cropCx * k, top: h / 2 - cropCy * k}} />
    </div>
  );
};

const PHONE_CROP: Record<string, [number, number, number]> = {
  'scr_hero.mp4': [617, 320, 315],
  'scr_mobile.mp4': [596, 320, 250],
};

export const Screen: React.FC<SceneProps> = ({scene, lockups}) => {
  const f = useCurrentFrame();
  const dur = scene.to - scene.from;
  const src: string = scene.src;
  const rate = rateFor(src, dur);
  if (scene.phone) {
    const [cx, cy, cw] = PHONE_CROP[src];
    return (
      <AbsoluteFill>
        <NavyBg />
        <PhoneCard src={src} cropCx={cx} cropCy={cy} cropW={cw} f={f} dur={dur} />
      </AbsoluteFill>
    );
  }
  // carte desktop, éventuellement transformée en téléphone (mobile-first)
  let t = 0;
  if (scene.morph) {
    let at = Math.round(dur * 0.3);
    for (const l of lockups) for (const w of l.words) if (/mobile/i.test(w.text)) at = l.from + w.at - scene.from;
    t = interpolate(f, [at, at + 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  }
  const [pcx, pcy, pcw] = PHONE_CROP['scr_hero.mp4'];
  const cw = interpolate(t, [0, 1], [980, 500]);
  const ch = interpolate(t, [0, 1], [524, 1000]);
  const top = interpolate(t, [0, 1], [560, 230]);
  const radius = interpolate(t, [0, 1], [26, 60]);
  const push = interpolate(f, [0, dur], [1, 1.06]);
  const k = interpolate(t, [0, 1], [980 / SW, 500 / pcw]) * push;
  const cx = interpolate(t, [0, 1], [SW / 2, pcx]);
  const cy = interpolate(t, [0, 1], [SH / 2, pcy]);
  return (
    <AbsoluteFill>
      <NavyBg />
      <div style={{...PHONE_FRAME, left: (1080 - cw) / 2, top, width: cw, height: ch, borderRadius: radius,
        boxShadow: `0 0 0 ${12 * t}px #0B0D14, 0 0 140px 20px rgba(40,90,255,0.35), 0 50px 100px rgba(0,0,0,0.6)`}}>
        <OffthreadVideo src={Asset(src)} muted playbackRate={rate} startFrom={Math.round((CLIP_START[src] ?? 0) * 30)}
          style={{position: 'absolute', maxWidth: 'none', width: SW * k, height: SH * k, left: cw / 2 - cx * k, top: ch / 2 - cy * k}} />
      </div>
    </AbsoluteFill>
  );
};
