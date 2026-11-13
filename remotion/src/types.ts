export type Style = 'base' | 'b' | 'i' | 's' | 'x' | 'm' | 'g';
export type Word = {text: string; style: Style; at: number};
export type Lockup = {from: number; to: number; scene: number; quoted: boolean; hidden: boolean; words: Word[]};
export type Scene = {
  type: string;
  from: number;
  to: number;
  idx: number;
  srcStart: number;
  [k: string]: any;
};
export type ShortData = {
  id: string;
  titre: string;
  fps: number;
  durationInFrames: number;
  voiceEnd: number;
  voice: {src0: number; src1: number; from: number}[];
  scenes: Scene[];
  lockups: Lockup[];
  cta: {from: number; to: number; word: string; line: string};
};
export type SceneProps = {scene: Scene; data: ShortData; lockups: Lockup[]};
