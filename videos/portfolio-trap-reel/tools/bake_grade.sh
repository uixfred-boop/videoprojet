#!/usr/bin/env bash
# Bake the footage correction into the files (run from the project root).
#
# The footage (the user's 1008_18 clip) is already well exposed, and `hyperframes media-treatment --analyze` saw no
# imbalance. The user asked on the previous reel for truly black hair and t-shirt and no yellow cast, so this is only a
# gentle anchor, built into a 3D LUT by the canonical parametric builder (`hyperframes media-use resolve --type lut
# --params`, values in tools/grade.json):
# - blacks -0.08 with exposure +0.04: the black t-shirt goes from Y≈15 to ≈13 without darkening the face;
# - no temperature change: the wall is warm on one side and neutral on the other, so a global shift turned it cyan;
# - a shadows-only split tone (red +0.004, blue -0.018) takes the navy out of the t-shirt so black stays neutral;
# - vibrance +0.03, then a light luma unsharp (5x5, 0.6).
# The cutout gets the identical chain, plus a choked alpha so its soft matte draws no wall-coloured rim.
# The raw files stay next to the graded ones (desk-raw.mp4, desk-cutout-raw.webm).
set -euo pipefail
PARAMS=$(python3 -c 'import json; print(json.dumps(json.load(open("tools/grade.json"))["adjust"]))')
SPLIT='{"intensity":1,"balance":0.25,"shadows":[0.004,0,-0.018],"highlights":[0,0,0]}'
LUT_PARAMS=$(python3 -c 'import json, sys; p = json.loads(sys.argv[1]); p["splitTone"] = json.loads(sys.argv[2]); print(json.dumps(p))' "$PARAMS" "$SPLIT")
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
npx hyperframes media-use resolve --type lut --params "$LUT_PARAMS" --project "$TMP" --json > "$TMP/lut.json"
CUBE=$(python3 -c 'import json, sys; print(sys.argv[1] + "/" + json.load(open(sys.argv[1] + "/lut.json"))["path"])' "$TMP")
GRADE="scale=in_color_matrix=bt709:in_range=tv,format=gbrp16le,lut3d=file=${CUBE}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv"
SHARPEN="unsharp=5:5:0.6:5:5:0"
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
