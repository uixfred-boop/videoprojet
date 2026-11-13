import React from 'react';
import {AbsoluteFill, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {SceneProps} from '../types';
import {NavyBg} from './common';

// Visage en carte arrondie (cadrage B validé). Le rush est 1920x1080 ; on montre une zone 800x880/zoom.
const CARD = {x: 90, y: 300, w: 900, h: 990};

export const FaceCard: React.FC<{srcStart: number; pieces?: {from: number; src: number}[]; cx?: number; cy?: number; zoom?: number; cxAt?: number[][]; dur: number; revealAt?: number}> = ({srcStart, pieces, cx = 895, cy = 480, zoom = 1, cxAt, dur, revealAt = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  let centerX = cx;
  if (cxAt) for (const [at, x] of cxAt) if (f >= at) centerX = x;
  const drift = interpolate(f, [0, Math.max(1, dur)], [1, 1.035]);
  const z = zoom * drift;
  const k = (CARD.w / 800) * z;
  const regionW = CARD.w / k, regionH = CARD.h / k;
  const left = -(centerX - regionW / 2) * k;
  const top = -(cy - regionH / 2) * k;
  // la carte apparaît quand le visage est vraiment à l'image dans le rush
  const rv = interpolate(f - revealAt, [0, 7], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (revealAt > 0 && f < revealAt) return null;
  return (
    <div
      style={{
        opacity: revealAt > 0 ? rv : 1, transform: revealAt > 0 ? `scale(${0.965 + 0.035 * rv})` : undefined,
        position: 'absolute', left: CARD.x, top: CARD.y, width: CARD.w, height: CARD.h, borderRadius: 34, overflow: 'hidden',
        boxShadow: '0 0 120px 10px rgba(40,90,255,0.32), 0 40px 90px rgba(0,0,0,0.55)', background: '#000',
      }}
    >
      {(pieces && pieces.length ? pieces : [{from: 0, src: srcStart}]).map((p, i, arr) => (
        <Sequence key={i} from={p.from} durationInFrames={Math.max(1, (arr[i + 1]?.from ?? dur) - p.from)} layout="none">
          <OffthreadVideo
            src={staticFile('rush/rush.mp4')}
            startFrom={Math.max(0, Math.round(p.src * fps))}
            muted
            style={{position: 'absolute', left, top, width: 1920 * k, height: 1080 * k, maxWidth: 'none'}}
          />
        </Sequence>
      ))}
      <div style={{position: 'absolute', inset: 0, background: 'radial-gradient(90% 80% at 50% 40%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.35) 100%)'}} />
    </div>
  );
};

export const Face: React.FC<SceneProps> = ({scene}) => (
  <AbsoluteFill>
    <NavyBg />
    <FaceCard srcStart={scene.srcStart} pieces={scene.pieces} cx={scene.cx} cy={scene.cy} zoom={scene.zoom} cxAt={scene.cxAt} dur={scene.to - scene.from} revealAt={scene.revealAt} />
  </AbsoluteFill>
);
