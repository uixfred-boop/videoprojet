"""Render one talking-head clip at 4K: matte -> person over the room plate -> setup scale -> reframe -> grade.
usage: thclip.py <work> <src> <start> <end> <setup A|B|C> <zoom> <push 0|1> <out.mov> [shift]

Grade (v2, Fred's approved episode-1 look): the person keeps setup A's colour as shot (setups B and C are matched to A),
then gets `person_warm.cube` (= editing-style/lut/fred-warm-natural.cube: gentle S-curve, neutral shadows, slightly warm
highlights, +5 % saturation, no lifted blacks) and a light luma-only sharpen. The room plate carries its own moody look
(`plate4k_graded.png`, pre-graded once); nothing cool is applied over the skin. All RGB->YUV steps use BT.709."""
import json, math, subprocess, sys
work, src, s, e, setup, zoom, push, out = sys.argv[1:9]
SHIFT = float(sys.argv[9]) if len(sys.argv) > 9 else None   # side-panel layout: move the person horizontally (fraction of width)
s, e, zoom, push = float(s), float(e), float(zoom), int(push)
cfgs = json.load(open(f"{work}/setups.json")); cfg = cfgs[setup]
W, H, FPS = 3840, 2160, 30
dur = round((e - s) * FPS) / FPS
# Both inputs are seeked half a frame before the first wanted frame and re-timed by frame index. The matte files store
# millisecond timestamps (1/1000), the camera file exact 1/30 s ones: timing by PTS paired some frames with the previous
# frame's matte, which shows as a flickering rim on head moves.
k0 = math.ceil(s * FPS - 1e-9)
seek = (k0 - 0.5) / FPS
a_off = cfg["alpha_offset"]
sc = cfg["scale"]                       # person scale, anchored on the bottom edge (headroom + same size across setups)
pw, ph = int(W * sc) // 2 * 2, int(H * sc) // 2 * 2
px = int(W / 2 - pw / 2 + (SHIFT if SHIFT is not None else cfg.get("shift_x", 0)) * W) // 2 * 2
# white balance relative to setup A: A stays as shot (warm natural skin), B and C are pulled onto A
g = [cfg["gains"][i] / cfgs["A"]["gains"][i] for i in range(3)]
# camera zoom on the whole frame (person + room), anchored on the face; optional slow push-in (+4 % over the clip)
z = f"{zoom}+0.04*t/{dur:.3f}" if push else f"{zoom}"
fax, fay = cfg["face"]
TO709 = "scale=out_color_matrix=bt709:out_range=tv"
# setups A and B are matched onto setup C's skin tone and contrast (the look Fred picked): make_match.py -> match_A/B.cube
match = f"lut3d={work}/match_{setup}.cube:interp=tetrahedral," if setup in ("A", "B") else ""
fc = (
    f"[0:v]setpts=N/({FPS}*TB),unsharp=5:5:0.45:5:5:0,format=gbrpf32le,"
    f"colorchannelmixer=rr={g[0]:.4f}:gg={g[1]:.4f}:bb={g[2]:.4f},"
    f"lut3d={work}/person_warm.cube:interp=tetrahedral,{match}format=gbrp,scale={pw}:{ph}:flags=lanczos[fg];"
    f"[1:v]setpts=N/({FPS}*TB),format=gray,scale={W}:{H}:flags=bicubic,"
    f"lut=y='clip((val-{cfg.get('choke_lo', 28)})*255/{cfg.get('choke_rng', 210)},0,255)',scale={pw}:{ph}:flags=bicubic,split=3[a1][a2][a3];"
    f"[a1]format=gbrp[argb];[a3]format=gbrp[argb2];[fg][argb]blend=all_mode=multiply,format=gbrp[fgd0];"
    f"[fgd0][argb2]blend=all_mode=multiply:all_opacity={cfg.get('edge_extra', 0)},format=gbrp[fgd];"   # edge darkening: fg*a(*a), then *a by overlay
    f"[fgd][a2]alphamerge,{TO709},format=yuva444p[fga];"
    f"[2:v]loop=-1:size=1,trim=duration={dur + 0.2:.3f},setpts=PTS-STARTPTS,{TO709},format=yuv444p[bg];"
    f"[bg][fga]overlay=x={px}:y={H - ph + int(cfg.get('shift_y', 0) * H) // 2 * 2}:format=yuv444:shortest=1,"
    f"scale=w='trunc({W}*({z})/2)*2':h='trunc({H}*({z})/2)*2':eval=frame:flags=lanczos,"
    f"crop={W}:{H}:'(iw-{W})*{fax}':'(ih-{H})*{fay}',"
    f"vignette=angle=0.55:mode=forward,fps={FPS},format=yuv420p[v]"
)
af = f"afade=t=in:d=0.012,afade=t=out:st={dur - 0.015:.3f}:d=0.015"
cmd = ["ffmpeg", "-loglevel", "error", "-y",
       "-ss", f"{seek:.4f}", "-t", f"{dur + 0.2:.3f}", "-i", src,
       "-ss", f"{seek - a_off:.4f}", "-t", f"{dur + 0.2:.3f}", "-i", f"{work}/matte/{cfg['alpha']}",
       "-i", f"{work}/plate4k_graded.png",
       "-filter_complex", fc, "-map", "[v]", "-map", "0:a", "-af", af + f",atrim=0:{dur:.4f}", "-frames:v", str(round(dur * FPS)),
       "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-x264-params", "keyint=30",
       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1", out]
subprocess.run(cmd, check=True)
