# JUDGEMENT TALES — Production Repository

Production deliverables for **JUDGEMENT TALES**, an adult satirical animated comedy set in the bureaucratic afterlife.

**Produced by WANNATION MEDIA** — a division of **WANNATION HOLDINGS (PTY) LTD** · Reg No: **2026/463724/07**

> The **website** lives on Lovable (project **"Aftermath Antics"**, TanStack Start). This repo holds the writing, data and standards that drive the site and the animated production. Per the brief, **no MP4 files are committed here** — produced video is stored via Lovable Assets.

## Contents
| Path | What it is |
|---|---|
| `CONVENTIONS.md` | Show bible: credits, casting, satire guardrail, voice guide, episode architecture, data schema |
| `scripts/episode-01-the-queue.md` | **Full 10-minute pilot script** (3 skits, running order, credits, button gag) |
| `scripts/episodes-02-06-outlines.md` | Three-skit outlines for Episodes 2–6 |
| `social/cut-sheets.md` | TikTok / Reels / Shorts cut sheets (Ep 1 **VERIFIED** against the render; Ep 2–6 proposed) |
| `data/show-data.json` | Structured show data: slugs, skits, cast, artwork, running order, social cuts, production state |
| `production/content-standards.md` | SA legal + platform risk note (protects monetization) |
| `brand/watermark-spec.md` | Spinning WANNATION logo watermark spec (video + site) |
| **`PRODUCTION-NOTES.md`** | **Delivery report for the Ep 1 pilot: measured specs, open gaps, what the site still needs** |
| `pipeline/ep01/` | The reproducible CPU-only build that rendered the pilot (voice, score, picture) |
| `social/premiere-plan.md` | YouTube Premiere run-of-show, promo cadence and repurposing plan |

## Current production state (2026-11-21)
- **Ep 1 "The Queue" — `released`:** a **full 10:00 voiced, scored, subtitled animated pilot has been
  rendered and reviewed.** 600.00s / 1920x1080 / 24fps, 100 voiced lines, 2 embedded subtitle tracks,
  spinning WANNATION watermark, legal credits. Plus a **48.56s trailer** and **three 9:16 social cuts**.
  Read **[`PRODUCTION-NOTES.md`](PRODUCTION-NOTES.md)** for the measured specs, how it was made, and the
  honest list of open gaps — including the fact that it has **no character lip-sync** and that the
  **South African accent is not yet achieved** by the open-source voice set.
- **Ep 2-6:** still `script` (Ep 2-6 outlined). Ep 2 "Orientation Day" is unblocked but not started.
- **Nothing is uploaded.** `video.assetId` is `null` — the master is not on Lovable Assets or YouTube.
  The site must gate its player on `assetId` being non-null.
- Produced files live in `out/` (gitignored — no video binaries in the repo, per the brief).

## Source scene art
Reference frames supplied by the brief (Heavenly Reception / Orientation Day / Complaints Department / Downstairs Neighbours / The Numbers) map to episodes 1–6 in `data/show-data.json` → `artwork[]`.
