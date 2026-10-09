#!/usr/bin/env bash
# Bake the footage grade into the files (run from the project root).
#
# The footage was shot dark. The look was chosen and validated as a canonical treatment
# (tools/grade.json: exposure +0.35, shadows +0.3, via `npx hyperframes media-treatment`).
# In this GPU-less sandbox the realtime grade on ~18 videos crashed `hyperframes check`, so the same
# correction is baked into the files instead.
#
# The curve below was fitted to the treatment's own rendered output (per channel, quantile-matched on a
# strip frame; mean difference ~4 levels). The raw files stay next to the graded ones, so the original look
# is one copy away: cp desk-raw.mp4 desk.mp4 and cp desk-cutout-raw.webm desk-cutout.webm.
set -euo pipefail
CURVES="r='0.000/0.020 0.040/0.114 0.080/0.143 0.150/0.232 0.250/0.348 0.400/0.494 0.550/0.707 0.700/0.804 0.850/0.902 1.000/1.000':g='0.000/0.020 0.040/0.111 0.080/0.143 0.150/0.221 0.250/0.314 0.400/0.486 0.550/0.686 0.700/0.791 0.850/0.895 1.000/1.000':b='0.000/0.020 0.040/0.114 0.080/0.142 0.150/0.221 0.250/0.306 0.400/0.482 0.550/0.678 0.700/0.785 0.850/0.893 1.000/1.000'"
ffmpeg -nostdin -v error -y -i assets/video/desk-raw.mp4 -vf "curves=${CURVES}" -an \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -keyint_min 15 -movflags +faststart assets/video/desk.mp4
ffmpeg -nostdin -v error -y -c:v libvpx-vp9 -i assets/video/desk-cutout-raw.webm -vf "format=rgba,curves=${CURVES}" -an \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 22 -row-mt 1 -auto-alt-ref 0 assets/video/desk-cutout.webm
echo "baked: assets/video/desk.mp4, assets/video/desk-cutout.webm"
