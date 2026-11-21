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
| `social/marketing-plan.md` | Launch kit, P−7…P+14 posting calendar, paste-ready copy per clip |
| **`HANDOFF.md`** | **Current state for any agent (OpenCode, ChatGPT, Claude). Recompiled near every token limit** |

## Current production state (2026-11-21)
- **Ep 1 "The Queue" — v2 master rendered and verified (10/10 acceptance criteria).** Full 10:00,
  voiced, scored, captioned. **YouTube upload kit** in `out/youtube/`, **social launch kit** (trailer,
  five 9:16 clips, covers, key art) in `out/social/`. Details: **[`PRODUCTION-NOTES.md`](PRODUCTION-NOTES.md)**.
- **Agents: start with [`HANDOFF.md`](HANDOFF.md).**
- Open: no lip-sync; the South African accent is not achieved (placeholder voices); nobody has listened
  to it yet; nothing is uploaded (`video.assetId` is null); Ep 2–6 are scripts/outlines.
- Produced files live in `out/` (gitignored — no video binaries in the repo, per the brief).

## Source scene art
Reference frames supplied by the brief (Heavenly Reception / Orientation Day / Complaints Department / Downstairs Neighbours / The Numbers) map to episodes 1–6 in `data/show-data.json` → `artwork[]`.
