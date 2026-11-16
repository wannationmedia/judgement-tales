#!/usr/bin/env bash
# JUDGEMENT TALES — Stage 4: assemble an episode from motion clips.
# Stitches shots + voice track + subtitles + the spinning WANNATION watermark.
# Runs on CPU — works on any machine, including this Claude box (no GPU needed).
#
# Usage:
#   ./assemble.sh shots.txt voices.m4a subs.srt episode01.mp4
# where shots.txt is an ffmpeg concat list:
#   file 'shot1.mp4'
#   file 'shot2.mp4'
#   ...
set -euo pipefail
SHOTS="${1:?concat list (shots.txt)}"; AUDIO="${2:-}"; SUBS="${3:-}"; OUT="${4:-episode.mp4}"
HERE="$(cd "$(dirname "$0")" && pwd)"
LOGO="$HERE/logo.png"

# make the spinning logo mark once (ImageMagick), if missing
if [ ! -f "$LOGO" ]; then
  FB=/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf
  convert -size 500x500 xc:none \
    -fill '#12101c' -draw "circle 250,250 250,34" \
    -fill none -stroke '#e8c24a' -strokewidth 16 -draw "circle 250,250 250,44" \
    -stroke none -fill '#e8c24a' -font "$FB" -pointsize 150 -gravity center -annotate +0-6 'WN' \
    "$LOGO"
fi

# 1) concat the motion clips
ffmpeg -y -f concat -safe 0 -i "$SHOTS" -c:v libx264 -pix_fmt yuv420p -an _stitched.mp4

# 2) overlay spinning watermark (top-right, slow 25s/rotation) + burn subtitles if given
VF="[1:v]scale=140:140,rotate=2*PI*t/25:c=none:ow=rotw(iw):oh=roth(ih)[wm];[0:v][wm]overlay=W-w-40:40:format=auto:shortest=1[v0]"
if [ -n "$SUBS" ] && [ -f "$SUBS" ]; then
  VF="$VF;[v0]subtitles='$SUBS':force_style='FontName=DejaVu Serif,Fontsize=22,Outline=2'[v]"
else
  VF="$VF;[v0]copy[v]"
fi

# 3) mux with the voice track (no autoplay issues; real audio)
if [ -n "$AUDIO" ] && [ -f "$AUDIO" ]; then
  ffmpeg -y -i _stitched.mp4 -loop 1 -i "$LOGO" -i "$AUDIO" \
    -filter_complex "$VF" -map "[v]" -map 2:a \
    -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -shortest -movflags +faststart "$OUT"
else
  ffmpeg -y -i _stitched.mp4 -loop 1 -i "$LOGO" \
    -filter_complex "$VF" -map "[v]" \
    -c:v libx264 -crf 20 -pix_fmt yuv420p -an -movflags +faststart "$OUT"
fi
rm -f _stitched.mp4
echo "Wrote $OUT"
