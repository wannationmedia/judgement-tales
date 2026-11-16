# WANNATION Watermark Spec

Applies to every finished video **and** the site's video player.

| Property | Value |
|---|---|
| Asset | WANNATION logo (transparent PNG/SVG, supply master to `brand/`) |
| Position | **Top-right corner** (safe margin ≥ 3% of frame from edges; clear of subtitles) |
| Motion | **Slow, continuous spin on its own axis — one full rotation ≈ 20–30s.** Constant, no easing, never stops |
| Opacity | ~55–70% (visible, not distracting) |
| Size | ~7–9% of frame width |
| Social cuts | Keep the spinning watermark; ensure it survives the 9:16 crop (do not crop it out) |

## Implementations
**On finished video (FFmpeg, overlay a pre-rendered spinning logo loop):**
```bash
# 1) make a ~25s seamless spinning logo loop (transparent) from logo.png, then
ffmpeg -i episode.mp4 -stream_loop -1 -i wannation_spin_25s.mov \
  -filter_complex "[1:v]scale=iw*0.08:-1[wm];[0:v][wm]overlay=W-w-24:24:format=auto" \
  -c:a copy out.mp4
```
*(Produce `wannation_spin_25s.mov` once with an alpha codec, e.g. Remotion/After Effects/`rotate`-based render, then reuse.)*

**On the site player (CSS, over an HTML5 `<video>`):**
```css
.wn-watermark{position:absolute;top:3%;right:3%;width:8%;opacity:.65;
  animation:wn-spin 25s linear infinite;pointer-events:none}
@keyframes wn-spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.wn-watermark{animation:none}}
```
Note the reduced-motion fallback (accessibility): hold the logo static for users who request reduced motion.
