# Episode 1 "The Queue" — the build that produced the pilot

This is the exact, reproducible pipeline that rendered
`judgement-tales-s01e01-the-queue.mp4` (600.00s / 1920x1080 / 24fps / voiced / subtitled).

**It runs on CPU only.** No GPU, no paid service, no subscription. Everything is open source:
[Piper](https://github.com/OHF-Voice/piper1-gpl) for voice, NumPy for the score, FFmpeg + ImageMagick
for picture. The whole episode builds from the six approved scene plates in `images/`.

## Run it

```bash
pip install piper-tts numpy
```

```bash
mkdir -p .work/voices && cd .work/voices
python3 -m piper.download_voices en_GB-vctk-medium en_GB-alan-medium en_US-norman-medium \
  en_GB-northern_english_male-medium en_US-l2arctic-medium en_GB-jenny_dioco-medium \
  en_GB-cori-high en_US-reza_ibrahim-medium en_GB-alba-medium en_US-amy-medium
```

```bash
cd pipeline/ep01
python3 gen_voices.py      # 1. synthesize + treat all 100 dialogue lines, measure real durations
python3 layout.py          # 2. lay the measured audio on a timeline, solve for exactly 10:00
python3 build_audio.py     # 3. place dialogue, lay the score, duck, normalise to -16 LUFS
python3 prepare_plates.py  # 4. cut 39 framings out of the 6 approved plates
python3 make_brand.py && python3 make_cards.py && python3 make_props.py
python3 render_shots.py    # 5. render 219 cuts with camera moves + practical gags (~20 min, 4 cores)
python3 make_subs.py       # 6. SRT + VTT, clean and SDH, from the measured audio
python3 assemble.py        # 7. concat, grade, spin the watermark, mux audio + soft subs
python3 select_cuts.py && python3 make_social.py   # 8. trailer + 9:16 social cuts
```

## What each file owns

| File | Owns |
|---|---|
| `cast.py` | Voice cast: model, speaker id, rate, pitch shift, EQ per character |
| `timeline.py` | **The episode.** Every line, beat and card. `txt` = what the engine says, `sub` = what the subtitle shows |
| `shots.py` | The 39 framings — each a 16:9 window onto an approved plate |
| `layout.py` | Solves beat lengths so the episode lands on exactly 600.00s; expands held beats into real cuts |
| `synth.py` | The original score: Karplus-Strong harp, lounge muzak, tape warble, and every spot effect |
| `build_audio.py` | Dialogue placement, score beds, sidechain ducking, loudness |
| `render_shots.py` | Per-cut camera motion + the flip-board / lunch-sign / golden-pass overlays |
| `assemble.py` | Concat → retro grade (scanlines, grain, vignette) → spinning watermark → mux |
| `make_subs.py` | Timed from the **measured** audio, so sync is correct by construction |
| `f0.py` | Pitch measurement used to cast voices to distinct timbres |

## Why it looks the way it does

The six plates are stills. The motion is real but **limited/cutout**: a camera move on every
cut, 219 cuts at a 2.62s average, composited practical props for the gags, and a retro
broadcast grade. There is **no character lip-sync** — see `PRODUCTION-NOTES.md` for the
honest list of what that does and does not give you.
