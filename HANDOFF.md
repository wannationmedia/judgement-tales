# HANDOFF — JUDGEMENT TALES (for OpenCode, ChatGPT, or a fresh Claude session)

> **Standing rule (from the owner):** this file is recompiled **every time an agent nears its
> token/context limit**, and before any handoff. Overwrite it with the current state; keep it
> self-contained — the next agent gets this file and the repo, nothing else.

**Last compiled:** 2026-11-21 21:34 · branch `claude/dazzling-bell-7lfk6a` · base `claude/amazing-hamilton-tq8zt4`
(the repo has **no `main`** — the default branch is `claude/amazing-hamilton-tq8zt4`).

---

## 1. What this project is

Adult animated satirical comedy, **JUDGEMENT TALES** — a bureaucratic afterlife run like Home Affairs.
Produced by **WANNATION MEDIA**, a division of **WANNATION HOLDINGS (PTY) LTD**, Reg No **2026/463724/07**
(this exact credit goes on everything). Show bible: `CONVENTIONS.md`. Pilot script:
`scripts/episode-01-the-queue.md`. Website lives in a separate Lovable project ("Aftermath Antics")
that **no agent here can reach**.

## 2. Where things stand

| Item | State |
|---|---|
| Ep 1 pilot v1 (10:00, voiced, subtitled) | **Merged** — PR #1 |
| Cognitive walkthrough of v1 | Done: 5/10 steps passed, 7 findings (F1–F7) |
| **Fixes F1–F7 in the pipeline** | **Done** (in `.work/build/`, not yet copied to `pipeline/ep01/`) |
| **v2 re-render** | **IN PROGRESS** — `.work/rebuild.sh` running in background; 95/212 clips at handoff |
| YouTube package (`out/youtube/`) | Thumbnails A/B/C, `title.txt`, `description.txt` (with chapters), `tags.txt`, `chapters.json`, `UPLOAD.md` — **done** |
| Key art (`out/social/key-art/`) | Channel banner, profile mark, square/portrait posts, launch story — **done** |
| Social verticals + vertical trailer | **NOT built yet** — run after the master (step 4 below) |
| `social/marketing-plan.md` | Written, uncommitted |
| Docs/data/commit/PR for v2 | **Not done** |

## 3. What v2 fixes (walkthrough findings)

- **F1** Nigel's voice was heard over other characters' faces (8 lines). No lip-sync exists, so the face on
  screen is the *only* speaker cue. Now Nigel is only ever on the `alcove` or inserts. Verified: 0 mismatches.
- **F2** The caper's object, Sven's horned helmet, didn't exist on screen. Now composited on him from his first shot.
- **F3** Sven sat in a boardroom, not the queue. Now cut out (rembg `isnet-anime`) and staged in Heavenly
  Reception, including a two-shot with Lwazi.
- **F4** Punchline sign "GONE TO LUNCH — BACK IN ETERNITY" was legible 1.5s; now 5.0s and captioned.
- **F5** Auto-coverage cut to Moses at a door mid-reception. Coverage pools are now keyed by **scene**, not source image.
- **F6** Caption track "English (SDH)" → "English — speaker names & sounds".
- **F7** Cold open was ~10s of black. Now opens on the reception (NOW SERVING 046) and the voice-over is set as type.
- Also: Skit A title card added; Brenda's wide crop no longer spoils Moses' tablets; helmet-lift gag animates the
  theft attempts in the Skit B montage.

## 4. Exactly what to do next

```bash
# 0. Is the render still going?  (rebuild = audio -> plates -> props -> 212 clips -> subs -> master)
ls .work/clips | wc -l ; tail -3 .work/rebuild.log ; pgrep -f rebuild.sh
# If it died: just re-run it (idempotent). ONLY ONE COPY AT A TIME — two copies race on the same files.
bash .work/rebuild.sh > .work/rebuild.log 2>&1
```

```bash
# 1. Verify the master against the 10 acceptance criteria (must print 10/10)
cd .work/build && python3 verify_walkthrough.py
```

```bash
# 2. Look at frames yourself (helmet on Sven, sign readable, no black cold open)
for t in 2 8 130 300 535; do ffmpeg -v error -ss $t -i ../../out/judgement-tales-s01e01-the-queue.mp4 -frames:v 1 /tmp/f$t.jpg -y; done
```

```bash
# 3. Social: trailer (16:9), 5 verticals, vertical trailer, covers  -> out/social/
python3 select_cuts.py && python3 make_social.py
```

```bash
# 4. Copy the pipeline into the repo, including the Sven cutout tools
cp .work/build/*.py pipeline/ep01/ ; mkdir -p pipeline/ep01/cutout ; cp .work/cutout/{make_sven.py,helmet.sh,stage_sven.py} pipeline/ep01/cutout/
```

5. Update `data/show-data.json` (ep1 `runningOrder` from `.work/cuts.json`, `socialCuts` from `.work/social_built.json`,
   `trailer`), `social/cut-sheets.md`, `PRODUCTION-NOTES.md` (v2 + walkthrough result), `README.md`.
6. Commit on `claude/dazzling-bell-7lfk6a`, push, open a **draft PR into `claude/amazing-hamilton-tq8zt4`**.
   **No video/audio files in git** (`.gitignore` blocks them; `out/` and `.work/` are ignored).
7. Prepend an entry to `/root/tasks/judgement-tales-pilot/LOGBOOK.md` (Baton), then recompile this file.

## 4b. If you are on a FRESH CLONE (no `.work/`)

`.work/` and `out/` are gitignored, so a clone has only the code. The full pipeline is mirrored in
`pipeline/ep01/` (cutout tools in `pipeline/ep01/cutout/`). Scripts use absolute paths under
`/home/user/judgement-tales/` — fix `ROOT`/`REPO` constants if your checkout lives elsewhere. Rebuild order:

```bash
pip install piper-tts "rembg[cpu]" numpy pillow     # plus system ffmpeg + imagemagick
mkdir -p .work/build .work/voices && cp pipeline/ep01/*.py .work/build/
(cd .work/voices && python3 -m piper.download_voices en_GB-vctk-medium en_GB-alan-medium en_US-norman-medium \
  en_GB-northern_english_male-medium en_US-l2arctic-medium en_GB-jenny_dioco-medium en_GB-cori-high \
  en_US-reza_ibrahim-medium en_GB-alba-medium en_US-amy-medium)
cd .work/build && python3 gen_voices.py && python3 layout.py && python3 prepare_plates.py
# Sven: cut out + helmet + staging (needs .work/cutout/sven_src.png: crop 440x470+0+190 of images/6.jpg)
mkdir -p ../cutout ../props && convert ../../images/6.jpg -crop 440x470+0+190 +repage ../cutout/sven_src.png
cp ../../pipeline/ep01/cutout/* ../cutout/ && (cd ../cutout && python3 -c "from rembg import remove,new_session;from PIL import Image;remove(Image.open('sven_src.png'),session=new_session('isnet-anime')).save('sven_cut.png')" && python3 make_sven.py && bash helmet.sh && python3 stage_sven.py)
python3 make_brand.py && python3 make_cards.py && bash ../../pipeline/ep01/rebuild.sh
```

## 5. File map

| Path | What |
|---|---|
| `.work/build/` | **Live pipeline** (edit here, then copy to `pipeline/ep01/`) |
| `.work/build/timeline.py` | The episode: every line/beat/card. `txt` = spoken (phonetic), `sub` = displayed |
| `.work/build/shots.py` | Framings + `FACES` map (who is visible in each shot) |
| `.work/build/layout.py` | Solves timing to exactly 600.00s; `hold=True` beats are never stretched/split |
| `.work/cutout/` | Sven cutout, helmet drawing, staging into reception |
| `.work/plates/` | 2880×1620 plates; `sven_*`, `helmet_*` are **pre-built** (`p="PRE"`) |
| `out/` | Deliverables: master, SRT/VTT, `youtube/`, `social/` |
| `/root/tasks/judgement-tales-pilot/LOGBOOK.md` | Session-by-session record |

Tools: Piper TTS (`pip install piper-tts`, voices in `.work/voices/`), rembg, NumPy, FFmpeg, ImageMagick. CPU only, no GPU.

## 6. Traps already paid for — don't repeat

- `-shortest` when muxing subtitles truncates the episode to the last caption cue. Use `-t 600`.
- A `-loop 1` image input never ends: **always** cap renders with `-t` and `-frames:v`.
- ImageMagick `tile:` flattens alpha — the old scanline overlay blacked out the whole picture.
- Every cut must hold through the pause after its line (`vdur`), or the picture runs short of the audio.
- `gblur` at high sigma on 1080×1920 is ~50× slower than downscale → blur → upscale.
- Timeline indices key the voice files: after inserting/removing events, re-run `gen_voices.py`.
- Background jobs: check the *right* process name before concluding one died.

## 7. Honest open gaps (do not paper over)

- **No lip-sync** anywhere. Needs a GPU talking-head stage.
- **South African accent not achieved** — no SA English voice in the open Piper set. Voices are placeholders; recast before release.
- Nigel has no art (deliberately never seen). Sven's art is a composite, not new character design.
- Nothing uploaded: `video.assetId` is null. Website work (episode pages, `/episodes/$slug`) is in the unreachable Lovable project.
- Nobody has *listened* to the episode. A human must watch it with sound before publishing.
- Episode 2 not started.
