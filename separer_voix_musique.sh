#!/usr/bin/env bash
# Sépare la voix et la musique de fond d'une vidéo (ou d'un fichier audio)
# avec Demucs (modèle htdemucs_ft).
#
# Usage : ./separer_voix_musique.sh <video_ou_audio> [dossier_sortie]
#
# Prérequis : ffmpeg, et un environnement Python avec torch + demucs :
#   python3 -m venv venv
#   ./venv/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch torchaudio
#   ./venv/bin/pip install demucs soundfile
#
# Si le téléchargement automatique des poids échoue, placez les fichiers
# htdemucs_ft (04573f0d-f3cf25b2.th, 92cfc3b6-ef3bcb9c.th, d12395a8-e57c48e6.th,
# f7e0c4bc-ba3fe64a.th, htdemucs_ft.yaml) dans un dossier et passez-le via
# DEMUCS_REPO=/chemin/vers/models.
set -euo pipefail

src="${1:?Usage: $0 <video_ou_audio> [dossier_sortie]}"
out="${2:-sortie}"
python="${PYTHON:-./venv/bin/python}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

mkdir -p "$out"

# 1. Extraire la piste audio en WAV stéréo 44,1 kHz
ffmpeg -v error -y -i "$src" -vn -ac 2 -ar 44100 -c:a pcm_s16le "$work/audio.wav"

# 2. Séparer voix / reste (= musique de fond) avec Demucs
repo_args=()
[ -n "${DEMUCS_REPO:-}" ] && repo_args=(--repo "$DEMUCS_REPO")
"$python" -m demucs "${repo_args[@]}" -n htdemucs_ft --two-stems=vocals \
  --float32 -o "$work/sep" "$work/audio.wav"

stems="$work/sep/htdemucs_ft/audio"

# 3. Exporter : FLAC (sans perte) + MP3 320 kb/s
for pair in "vocals:voix" "no_vocals:musique_fond"; do
  stem="${pair%%:*}"; name="${pair##*:}"
  ffmpeg -v error -y -i "$stems/$stem.wav" -af aresample=osf=s16:dither_method=triangular -c:a flac "$out/$name.flac"
  ffmpeg -v error -y -i "$stems/$stem.wav" -c:a libmp3lame -b:a 320k "$out/$name.mp3"
done

echo "Fichiers créés dans $out/ :"
ls -lh "$out"
