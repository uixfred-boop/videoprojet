#!/bin/bash
# Remplace la musique de fond des 6 shorts V2 par un son fourni, sans re-rendre les images.
# Usage : ./swap_music.sh <fichier_son> [début_en_secondes]
#   - le son est converti en WAV 48 kHz et son niveau est aligné sur celui du beat (même mixage sous la voix)
#   - seule la piste audio est recalculée (voix isolée + son + bruitages), puis recollée sur la vidéo V2
set -euo pipefail
SRC="$1"; START="${2:-0}"
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
R="$ROOT/remotion"; OUT="$ROOT/rendus/fred-portfolio-7000-V2-son"; mkdir -p "$OUT" "$R/out/audio_swap"
ffmpeg -nostdin -v error -i "$SRC" -vn -ac 2 -ar 48000 "$R/public/audio/user_music.wav" -y
# niveau intégré du son fourni vs beat de référence (-8.8 LUFS) → gain
L=$(ffmpeg -nostdin -ss "$START" -i "$R/public/audio/user_music.wav" -af ebur128=framelog=quiet -f null - 2>&1 | awk '/^ +I:/{v=$2} END{print v}')
GAIN=$(python3 -c "print(round(10**((-8.8 - ($L))/20), 3))")
echo "son fourni : $L LUFS → gain $GAIN"
names=("" "01_the-7000-question" "02_millions-of-views-zero-clients" "03_why-i-chose-construction" "04_dont-add-remove" "05_details-nobody-notices" "06_have-a-clear-persona")
cd "$R"
for i in 1 2 3 4 5 6; do
  REMOTION_MUSIC=audio/user_music.wav REMOTION_MUSIC_START="$START" REMOTION_MUSIC_GAIN="$GAIN" \
    npx remotion render src/index.ts short$i "out/audio_swap/short$i.wav" --codec=wav --log=error < /dev/null
  ffmpeg -nostdin -v error -i "out/final/short$i.mp4" -i "out/audio_swap/short$i.wav" -map 0:v -map 1:a -c:v copy \
    -af loudnorm=I=-14:TP=-1.0:LRA=11 -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart "$OUT/${names[$i]}.mp4" -y
  echo "${names[$i]} ok"
done
