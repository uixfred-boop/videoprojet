import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {C, FONT} from '../theme';

export const NavyBg: React.FC<{halo?: boolean}> = ({halo = true}) => (
  <AbsoluteFill
    style={{
      background: halo
        ? `radial-gradient(90% 55% at 50% 40%, #12307A 0%, ${C.navy} 48%, ${C.navyDeep} 100%)`
        : `linear-gradient(180deg, ${C.navy} 0%, ${C.navyDeep} 100%)`,
    }}
  />
);

export const BlueBg: React.FC = () => (
  <AbsoluteFill style={{background: `radial-gradient(110% 70% at 50% 45%, #1A5CFF 0%, ${C.blue} 55%, #0036D6 100%)`}} />
);

export const PaperBg: React.FC = () => <AbsoluteFill style={{background: C.paper}} />;

// Grain animé : tuiles de bruit pré-calculées, changées toutes les 2 images
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.07}) => {
  const f = useCurrentFrame();
  const k = Math.floor(f / 2) % 6;
  return (
    <AbsoluteFill
      style={{
        backgroundImage: `url(${staticFile(`assets/grain${k}.png`)})`,
        backgroundSize: '256px 256px',
        opacity,
        mixBlendMode: 'overlay',
        pointerEvents: 'none',
      }}
    />
  );
};

export const Vignette: React.FC<{strength?: number}> = ({strength = 0.55}) => (
  <AbsoluteFill style={{background: `radial-gradient(75% 60% at 50% 45%, rgba(0,0,0,0) 40%, rgba(0,0,0,${strength}) 100%)`}} />
);

export const BigNumber: React.FC<{text: string; y: number; size: number; color?: string}> = ({text, y, size, color = '#FFFFFF'}) => (
  <div
    style={{
      position: 'absolute',
      top: y,
      left: 0,
      right: 0,
      textAlign: 'center',
      transform: 'translateY(-50%)',
      fontFamily: FONT.sans,
      fontWeight: 900,
      fontSize: size,
      letterSpacing: '-0.06em',
      lineHeight: 1,
      backgroundImage: `linear-gradient(180deg, ${color} 25%, rgba(255,255,255,0) 100%)`,
      WebkitBackgroundClip: 'text',
      backgroundClip: 'text',
      color: 'transparent',
    }}
  >
    {text}
  </div>
);

export const Asset = (name: string) => staticFile(`assets/${name}`);
export {Img};
