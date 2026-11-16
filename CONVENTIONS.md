# JUDGEMENT TALES — Show Bible & Project Conventions

> **Series:** JUDGEMENT TALES — an adult satirical animated comedy set in the bureaucratic afterlife.
> **Produced by:** **WANNATION MEDIA**, a division of **WANNATION HOLDINGS (PTY) LTD** · Reg No: **2026/463724/07**
> **Format:** Animated episodic comedy, ~10 min/episode, landscape (16:9) for YouTube, with vertical social cut-downs.
> **Tone reference:** *American Dad* (look & cartoon logic) × *Snatch* (interlocking, fast, quirky caper dialogue).
> **Look:** Retro public-access-television / cable-broadcast aesthetic, preserved from the existing site.

This repository holds the **production deliverables** (scripts, cut sheets, show data, standards). The **website** is the Lovable project **"Aftermath Antics"** (TanStack Start). Per the brief, no MP4 files are committed here — produced video is stored via Lovable Assets.

---

## 1. Credit & attribution (hard requirement)

- Company credit is **WANNATION MEDIA** throughout the site and on every new video credit sequence. This **replaces Owenation Media** wherever it appears.
- Full legal credit line for credits/footers:
  **WANNATION MEDIA — a division of WANNATION HOLDINGS (PTY) LTD · Reg No: 2026/463724/07**
- **WANNATION logo watermark:** bottom/top-**right corner**, semi-transparent, **gently and continuously spinning on its own axis, very slowly** (one rotation ≈ 20–30s). Present on all finished video and on the site's video player. See `brand/watermark-spec.md`.

## 2. Casting (creative interpretations — NOT historical or factual claims)

| Role | Casting | Function in the show |
|---|---|---|
| **God** | Black | Distant executive / board chair. Rarely intervenes; speaks in KPIs. |
| **Jesus** | Chinese | Warm corporate trainer; runs Orientation Day. Relentlessly on-message. |
| **Moses** | Iranian / Persian | Weary veteran who runs the Complaints Department. Carries stone tablets of grievances. |
| **St. Peter** | Old-world European | Reception clerk / gatekeeper. Fussy, rubber-stamp bureaucrat. |
| **Ottoman court figures** | Black (fictional casting) | "Downstairs Neighbours" / visiting dignitaries. Grand, theatrical. |

**Standing note required on-site and in docs:** These casting choices are **creative, fictional interpretations for a comedy**, not claims that any historical population was uniformly of one race, and not a statement about anyone's faith.

## 3. Satire guardrail (protects monetization + legal standing)

The target of the satire is **bureaucracy, power, management, admin, and individual characters** — never a religious group, race, or nationality as a group.

- ✅ Jokes at: queues, HR, middle-management, forms, KPIs, call-centres, red tape, self-importance, the absurdity of eternity run like an office.
- ❌ Avoid: "this religion is false/stupid," mockery of worshippers or sacred practice, slurs, group blame, dehumanising a nationality or race.
- Religious figures are reimagined as **overworked, dignified civil servants** — affectionate, not demeaning.
- Rationale: South African **Equality Act (PEPUDA)** hate-speech provisions, the **Films and Publications Act** classification regime, and **YouTube** hate-speech/monetization policy all protect *satire of power* but penalise *attacks on a group*. Staying on the right side of this line keeps the channel live and earning. Full note: `production/content-standards.md`.

## 4. Language & voice ("Mind Your Language" blend, dominant SA accent)

- **Primary language:** English.
- **Dominant accent:** **South African** (the POV protagonist and the show's "home" voice).
- **Ensemble:** an international cast of the newly-dead and heaven's staff, each with a distinct accent, in the spirit of the classic sitcom *Mind Your Language* — comedy from **register and accent clashes**, with everyone's dignity intact. The joke is the bureaucracy they're all trapped in, not their origin.
- Subtitles: synchronized **English** subtitles on all finished video (accessibility + reach).

### Voice quick-reference
| Character | Accent / register | Signature |
|---|---|---|
| **Lwazi "Lucky" Nkosi** (protagonist) | Joburg South African English | "Eish", "yoh", "sharp-sharp", "just now", "ag no man", "my bru", deadpan |
| **St. Peter** | Fussy old-world European | "One does not simply…", form numbers, sighs |
| **Brenda** (Heavenly HR) | Clipped SA civil-servant | "Unfortunately", "as per policy", "take a ticket" |
| **Jesus** | Measured Chinese-English, trainer energy | "Great question", "let's circle back", slides |
| **Moses** | Weary Persian-English | "I have heard this one before", long pauses |
| **Nigel "The Blagger"** | Cockney wide-boy | "Listen, bruv", fast patter, dodgy deals |
| **Sven** (the Viking at 046) | Nordic lilt | Has waited since 862 AD; queue is his identity |
| **The Sultan** | Grand Levantine-English | Theatrical, third-person, "the Sultan does not queue" |

## 5. Episode architecture

Six episodes, each with its own page at **`/episodes/$slug`**. Make the existing `/episodes` route a **layout** with the schedule as an **index child**, so detail pages render.

| # | Slug | Title | Logline |
|---|---|---|---|
| 1 | `the-queue` | The Queue | Newly-dead Lwazi must survive Heaven's infinite processing line — and a black-market scheme to skip it. **(Pilot)** |
| 2 | `orientation-day` | Orientation Day | Jesus runs a soul-crushing corporate onboarding; Lwazi just wants the Wi-Fi password. |
| 3 | `the-complaints-department` | The Complaints Department | Moses processes 4,000 years of grievances; a new complaint breaks the system. |
| 4 | `downstairs-neighbours` | Downstairs Neighbours | A Heavenly Neighbours Potluck with the folks from Below goes sideways at the elevator. |
| 5 | `build-a-brighter-eternity` | Build a Brighter Eternity | Management rolls out a "transformation initiative"; the harps get an upgrade nobody asked for. |
| 6 | `the-numbers` | The Numbers | The afterlife's quarterly stats (the pie chart) don't add up, and someone has to answer for it. |

Each episode page carries: **artwork, synopsis, character appearances, full three-skit breakdown** (setup / action / comic payoff / dialogue), a **10-minute running order** with skit start/end timecodes incl. opening & closing credits, and **social cut sheets** (TikTok / Reels / Shorts) with in/out, length, captions. Timings are **PROPOSED** until verified against a finished render — always labelled as such.

## 6. Production states (honesty rule — no fake "aired")

Every episode/clip shows a truthful state. Never label an unrendered, silent, or unreviewed asset "aired" or "marketing-ready".

| State | Meaning |
|---|---|
| `script` | Script + skit breakdown complete; no video. |
| `art` | Scene artwork exists; no moving animation. |
| `in-production` | Animation/voice/subtitles being produced; not finished. |
| `teaser` | A short clip exists (labelled by real duration); full episode not done. |
| `released` | Full episode rendered, reviewed (runtime, voice, subtitle sync, credits) and playable. |

**Current reality (2026-11-16):** All six = `script` (Ep 1 full, Ep 2–6 outlined). Ep 1 pilot = staged production, targeting `teaser` tonight. None are `released`.

## 7. Data schema

See `data/show-data.json`. Each episode: `slug`, `number`, `title`, `logline`, `synopsis`, `status`, `runtimeTargetSec`, `cast[]`, `artwork[]`, `skits[]` (`setup`/`action`/`payoff`/`dialogueRef`), `runningOrder[]` (`label`/`startSec`/`endSec`), `socialCuts[]` (`platform`/`inSec`/`outSec`/`lengthSec`/`caption`/`timingVerified`), `video` (optional, `assetId`/`subtitlesAssetId` — populated only when actually produced).
