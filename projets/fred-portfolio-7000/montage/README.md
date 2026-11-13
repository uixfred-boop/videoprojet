# Montage des 6 shorts (V1)

## Reproduire le rendu
1. Mettre le rush dans `remotion/public/rush/rush.mp4` (la vraie copie, pas un lien symbolique : le serveur de Remotion ne les suit pas).
2. Isoler la voix : `python3 -m demucs --two-stems=vocals -n htdemucs rush.wav`, puis copier `vocals.wav` en `remotion/public/audio/voice.wav`.
3. Générer musique et bruitages : `python3 audio_gen.py ../../../remotion/public/audio`.
4. Générer les données : `python3 build.py`. Il lit `spec.py` et `../transcript/mots_alignes.json`, coupe les silences de plus de 0,4 s sur la voix isolée et écrit `remotion/src/data/shortN.json`.
5. Rendu : dans `remotion/`, lancer `npx remotion render src/index.ts short1 out/final/short1.mp4 --codec=h264 --crf=17 --audio-bitrate=320k`.

## Choix techniques
- **Cadrage** : visage en carte 900×990 sur fond bleu nuit. La carte apparaît (`revealAt`) seulement quand le visage est vraiment à l'écran dans le rush. Les passages couverts par un encart incrusté d'origine sont montés sans visage.
- **Son** :
  - la voix vient de Demucs (la musique d'origine est retirée) ;
  - la musique est une nappe ambient synthétisée par `audio_gen.py`, donc sans droits, environ 10 dB sous la voix ;
  - les bruitages sont discrets : souffle, clic, pop, montée vers l'appel à l'action.
- **Polices** : servies en local dans `public/fonts`, car le Chrome de rendu ne passe pas le proxy pour Google Fonts.
- **Images d'illustration** : Wikimedia Commons, uniquement CC0 et domaine public, donc sans crédit obligatoire :
  - `iran_workers.jpg` : « Construction workers in Iran 04 », CC0 ;
  - `nara_silhouettes.jpg` : NARA 556185, domaine public ;
  - `plimoth_framing.jpg` : « Plimoth Patuxet Construction 2025 », CC0 ;
  - `borovsky_house.jpg` : « Borovsky district new house construction », CC0 ;
  - `garage_house5.jpg` : « Post frame garage connected to traditional frame house-5 », CC0.
- **Captures du site** : extraites du rush, sans le cadre d'origine (`scr_*.mp4`).
