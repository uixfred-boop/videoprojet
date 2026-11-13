import React from 'react';
import {Composition} from 'remotion';
import {Short} from './Short';
import {ShortData} from './types';
import short1 from './data/short1.json';
import short2 from './data/short2.json';
import short3 from './data/short3.json';
import short4 from './data/short4.json';
import short5 from './data/short5.json';
import short6 from './data/short6.json';

const ALL = [short1, short2, short3, short4, short5, short6] as unknown as ShortData[];
// voix isolée par Demucs si disponible, sinon audio d'origine du rush
const VOICE = process.env.REMOTION_VOICE ?? 'audio/voice.wav';

export const Root: React.FC = () => (
  <>
    {ALL.map((d) => (
      <Composition key={d.id} id={d.id} component={Short as any} durationInFrames={d.durationInFrames} fps={30} width={1080} height={1920}
        defaultProps={{data: d, voiceSrc: VOICE}} />
    ))}
  </>
);
