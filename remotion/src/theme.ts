import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Charte du skill montage-minimal-premium (couleurs mesurées sur les références)
export const C = {
  blue: '#0047FF',
  blueSky: '#1782FD',
  navy: '#071233',
  navyDeep: '#04070F',
  halo: '#7698F4',
  paper: '#FBF8FC',
  ink: '#141115',
  inkSoft: '#5E5A66',
  red: '#C8102E',
};

// Polices servies en local (Google Fonts téléchargées dans public/fonts)
loadFont({family: 'Inter', url: staticFile('fonts/Inter-normal-500.woff2'), weight: '100 900', style: 'normal'});
loadFont({family: 'Instrument Serif', url: staticFile('fonts/InstrumentSerif-normal-400.woff2'), weight: '400', style: 'normal'});
loadFont({family: 'Playfair Display', url: staticFile('fonts/PlayfairDisplay-italic-600.woff2'), weight: '600', style: 'italic'});
loadFont({family: 'Playfair Display', url: staticFile('fonts/PlayfairDisplay-italic-700.woff2'), weight: '700', style: 'italic'});

export const FONT = {
  sans: 'Inter, system-ui, sans-serif',
  serif: '"Instrument Serif", Georgia, serif',
  italic: '"Playfair Display", Georgia, serif',
};

export const W = 1080;
export const H = 1920;
