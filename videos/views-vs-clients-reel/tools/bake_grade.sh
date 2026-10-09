#!/usr/bin/env bash
# Bake the footage grade into the files (run from the project root).
#
# The look is the canonical treatment in tools/grade.json, validated with `npx hyperframes media-treatment` and
# compared with `npx hyperframes grade-compare`. In this GPU-less sandbox the realtime grade on ~18 videos crashed
# `hyperframes check`, so the same `adjust` values are built into a 3D LUT by the canonical parametric builder
# (`hyperframes media-use resolve --type lut --params`) and baked here with ffmpeg.
#
# Round 2 (user feedback: "yellowish", "blurry", hair and t-shirt not "well black"):
# - no shadow lift, so the black point stays at 0 and hair and t-shirt stay deep black (blacks -0.25);
# - exposure +0.36 brightens the face and the wall instead;
# - temperature -0.24 / tint +0.02 neutralises the warm cast (the wall goes from beige to off-white);
# - vibrance +0.05 keeps the skin rich;
# - a shadows-only split tone (the builder's splitTone, blue -0.016) takes out the navy that the cooler balance
#   leaves in the hair, so black stays neutral;
# - then a light luma unsharp (5x5, 0.8) for crisper eyes, brows and hair, applied identically to both files.
# The cutout's soft matte carries wall colour in its outer edge, which drew a light rim around the hair against the
# dark background. Its alpha is choked (values under 100 drop out, the rest re-stretched), so the edge is hair.
#
# The conversions are explicit BT.709 (matrix, range, tags) in 16-bit RGB, so the browser decodes what was graded.
# The raw files stay next to the graded ones: cp desk-raw.mp4 desk.mp4 and cp desk-cutout-raw.webm desk-cutout.webm
# restores the original look.
set -euo pipefail
PARAMS=$(python3 -c 'import json; print(json.dumps(json.load(open("tools/grade.json"))["adjust"]))')
SPLIT='{"intensity":1,"balance":0.25,"shadows":[0,0,-0.016],"highlights":[0,0,0]}'
LUT_PARAMS=$(python3 -c 'import json, sys; p = json.loads(sys.argv[1]); p["splitTone"] = json.loads(sys.argv[2]); print(json.dumps(p))' "$PARAMS" "$SPLIT")
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
npx hyperframes media-use resolve --type lut --params "$LUT_PARAMS" --project "$TMP" --json > "$TMP/lut.json"
CUBE=$(python3 -c 'import json, sys; print(sys.argv[1] + "/" + json.load(open(sys.argv[1] + "/lut.json"))["path"])' "$TMP")
GRADE="scale=in_color_matrix=bt709:in_range=tv,format=gbrp16le,lut3d=file=${CUBE}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv"
SHARPEN="unsharp=5:5:0.8:5:5:0"
CHOKE="lut=a='clip((val-100)*255/155,0,255)'"
TAGS=(-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv)

ffmpeg -nostdin -v error -y -i assets/video/desk-raw.mp4 -an -vf "${GRADE},format=yuv420p,${SHARPEN}" \
  -c:v libx264 -preset slow -crf 15 -tune film -pix_fmt yuv420p -g 15 -keyint_min 15 "${TAGS[@]}" -movflags +faststart \
  assets/video/desk.mp4
# the cutout keeps its alpha: decode with libvpx, grade in RGBA, encode VP9 yuva420p (unsharp leaves alpha untouched,
# the choke only touches alpha)
ffmpeg -nostdin -v error -y -c:v libvpx-vp9 -i assets/video/desk-cutout-raw.webm -an \
  -vf "${GRADE/gbrp16le/gbrap16le},format=yuva420p,${SHARPEN},${CHOKE}" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 22 -row-mt 1 -auto-alt-ref 0 "${TAGS[@]}" assets/video/desk-cutout.webm
echo "baked: assets/video/desk.mp4, assets/video/desk-cutout.webm (LUT params ${LUT_PARAMS})"
