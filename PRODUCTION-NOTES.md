# JUDGEMENT TALES — S01E01 "The Queue": production delivery report

**Produced by WANNATION MEDIA · WANNATION HOLDINGS (PTY) LTD · Reg No: 2026/463724/07**
Build date: **2026-11-21**

This report separates **production delivery** (what was actually rendered) from
**website delivery** (what was not), as the brief requires.

---

## 1. Production delivery — ✅ DONE

### The pilot
`out/judgement-tales-s01e01-the-queue.mp4`

| Checked | Measured value |
|---|---|
| Runtime | **600.00s — exactly 10:00** (14,400 frames) |
| Picture | 1920×1080, 24 fps, H.264, ~6.0 Mbps, 433 MB |
| Audio | AAC 48 kHz stereo, **−15.8 LUFS integrated, −1.0 dBTP** |
| Dialogue | **100 voiced lines**, 9 distinct character voices, 175s of speech |
| Subtitles | 2 embedded tracks (English, English SDH) **+** 4 sidecar files (.srt/.vtt) |
| Subtitle sync | Verified: timed from the measured audio; RMS inside cues is **2.24×** RMS outside |
| Subtitle integrity | Muxed track compared to source SRT: **103 cues, 0 mismatches** |
| Watermark | WANNATION roundel, top-right, continuous 25s rotation, 66% opacity, full runtime |
| Credits | Scrolling cast + production roll, then the full legal card. Confirmed readable on frame |
| Cutting | **219 cuts**, 2.62s average shot length |

### Trailer and social cuts
| File | Real duration | Format |
|---|---|---|
| `judgement-tales-s01e01-trailer.mp4` | **48.56s** | 1920×1080 + soft English subs |
| `…-take-a-ticket-vertical.mp4` | **32.92s** | 1080×1920, burned captions, watermark |
| `…-eleven-hundred-years-vertical.mp4` | **28.75s** | 1080×1920, burned captions, watermark |
| `…-the-fast-track-vertical.mp4` | **42.29s** | 1080×1920, burned captions, watermark |

Every duration above is the **real measured duration** of the delivered file, not a target.

### Verified running order (replaces the proposed one)
| Segment | Start | End |
|---|---|---|
| Cold open — The Last Tuesday | 0:00.00 | 0:24.64 |
| Main titles | 0:24.64 | 0:42.64 |
| Skit A — Now Serving: 047 | 0:42.64 | 3:17.11 |
| Skit B — The Fast-Track | 3:17.11 | 6:00.72 |
| Skit C — Processing Error | 6:00.72 | 9:28.97 |
| Closing credits + button gag | 9:28.97 | 10:00.00 |

### How it was made
Entirely **open source, on CPU, with no paid service**: Piper (voice), NumPy (original score —
Karplus-Strong harp, lounge muzak, tape warble, every spot effect synthesized from scratch),
FFmpeg + ImageMagick (picture). Full reproducible build in `pipeline/ep01/`.

---

## 2. What this animation is — and is not

**It is** limited / cutout animation built from the six approved scene plates: a real camera
move on every one of the 219 cuts, fast cutting on the dialogue, composited practical props
that play the script's actual gags (the NOW SERVING board flipping 046 → 047, the
"GONE TO LUNCH — BACK IN ETERNITY" shutter sign, the golden Fast-Track Pass), and a retro
public-access broadcast grade (scanlines, grain, vignette).

**It is not** full character animation. There is **no lip-sync** — mouths do not move. That
needs a per-shot talking-head stage (SadTalker / LivePortrait) on a GPU, which this machine
does not have. The honest label for the current master is a **fully voiced, fully scored,
fully subtitled animatic-grade pilot cut**, not a frame-by-frame animated episode.

---

## 3. Open gaps — read before publishing

1. **The South African accent is not achieved.** The show bible (`CONVENTIONS.md` §4) makes
   Joburg SA the dominant accent and Lwazi the anchor voice. **No South African English voice
   model exists in the open Piper voice set.** Lwazi is currently a mid-range British male
   voice (VCTK speaker p271). Every other accent is an approximation too — Sven is a slowed,
   pitched-down American; Moses and the Sultan use Arabic-accented English models, not Persian
   or Levantine. **These are placeholder performances.** For a public release, recast with real
   voice actors, or fine-tune/clone voices on SA speech.
2. **Two characters have no art.** Sven is played by the warrior figure in plate 6; he has no
   horned helmet, which the script references. **Nigel is never seen at all** — handled as an
   off-screen voice with cutaways to what he is describing. That is a deliberate (and funny)
   choice that also happens to cover a gap: neither character has dedicated artwork yet.
3. **Nothing has been uploaded.** `video.assetId` and `subtitlesAssetId` are `null`. The master
   is not on Lovable Assets and not on YouTube. The site must gate its player on `assetId`
   being non-null, or it will advertise a video it cannot play.
4. **Episode 2 "Orientation Day" has not been produced.** The brief makes it conditional on the
   pilot succeeding. The pilot now exists, so Ep 2 is unblocked — but it is not started.
5. **The retro grade is warm.** It suits the public-access brief but is a creative choice worth
   a look on a calibrated screen before release.

---

## 4. Website delivery — ❌ NOT DONE (no access)

The brief's website work is **not delivered**, and not because it was skipped:

- Dedicated episode pages, the TanStack detail route at `/episodes/$slug`, making `/episodes`
  a layout with the schedule as an index child, the home-page trailer feature and latest-clips
  row, per-page titles/descriptions/social metadata — **all of that lives in the Lovable
  project "Aftermath Antics", which is not in this repository and which this session cannot
  reach.** This repo contains the writing, data and standards only (see `README.md`).
- What *was* delivered from here is the **data contract the site consumes**:
  `data/show-data.json` now carries the verified running order, the real social-cut timings
  with `timingVerified: true`, the `video` block (codec, runtime, loudness, subtitle files,
  watermark spec, `assetId: null`) and a `trailer` block.
- **Next step for the site:** upload the five files in `out/` to Lovable Assets, paste the
  returned asset pointers into `video.assetId` / `subtitlesAssetId` / `trailer.assetId`, then
  build the pages against this data.

Creating or publishing the YouTube channel is outside this update, per the brief. The files
are ready to upload when the channel is.

---

## 5. Satire guardrail — held

The target throughout is bureaucracy, power, admin and individual characters. Religious figures
are written and performed as overworked, dignified civil servants. The closing credits carry the
standing notice that the casting choices are creative interpretations, not historical or factual
claims about any population and not a statement about anyone's faith. The opening card carries a
short form of the same notice. See `production/content-standards.md`.
