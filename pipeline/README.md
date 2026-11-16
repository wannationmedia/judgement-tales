# JUDGEMENT TALES — Open-Source Animation Pipeline (free, self-hosted, no subscriptions)

**The honest setup.** AI video needs a GPU. This Claude cloud box has none (CPU only), so it cannot render frames here. But you do **not** need to pay any service. Everything below runs on **open-source models** on a **free GPU** (Google Colab / Kaggle) or your own GPU. This is the self-hosted, no-vendor-lock-in path you asked for.

## What "animated episode" actually needs (the real stack)
Turning your scene art into a talking, moving episode is a **multi-stage** job. Each stage is open-source and free:

| Stage | Job | Open-source tool (free) | GPU |
|---|---|---|---|
| 1. Voice | Script lines → character voices | **Coqui XTTS-v2** or **Piper** (TTS) | light / CPU-OK |
| 2. Scene motion | Still art → ambient camera/scene motion (~4s clips) | **Stable Video Diffusion (SVD)** or **AnimateDiff** or **LTX-Video** | GPU (free Colab T4 works) |
| 3. Talking mouths | Make a character's mouth move to the voice | **SadTalker** / **LivePortrait** / **Wav2Lip** | GPU |
| 4. Assemble | Stitch shots + voices + subtitles + spinning WANNATION watermark into the episode MP4 | **FFmpeg** | CPU (works anywhere, incl. here) |

> Reality check, no bullshit: **Stage 2 gives you cinematic motion of your scenes, not lip-sync.** Talking characters need Stage 3 on top. It's all doable and free, but it's a pipeline, not one button. A full voiced 10-min episode is many short clips assembled — same as every studio does it.

## Fastest way to see your art MOVE for free (today)
1. Open Google Colab → new notebook → Runtime → **Change runtime type → T4 GPU** (free tier).
2. Upload `animate_scene.py` and one of your scene images (e.g. `images/1.jpg`).
3. Run:
   ```bash
   !pip -q install "diffusers>=0.27" transformers accelerate imageio imageio-ffmpeg
   !python animate_scene.py --image 1.jpg --out shot1.mp4 --motion 120
   ```
4. Download `shot1.mp4` — that's your Heavenly Reception scene actually moving. ~2–4 min on the free GPU.

Then Stage 4 (`assemble.sh`, runs even here on CPU) adds voices, subtitles and the spinning watermark.

## Two ways to run the whole thing
- **Free GPU (recommended for your limited workstation):** Google Colab free T4, or Kaggle (30 free GPU hrs/week). Zero cost, zero install on your PC.
- **Your own GPU:** any NVIDIA card with ≥8 GB VRAM (e.g. RTX 3060 12 GB) runs SVD/AnimateDiff locally. On a weak/no GPU, use Colab.

## Files in this folder
- `animate_scene.py` — Stage 2: Stable Video Diffusion, still → motion clip. Runnable on free Colab now.
- `assemble.sh` — Stage 4: FFmpeg stitch + audio + subtitles + spinning WANNATION watermark. Runs on CPU (even in this box).
- `ep1_shots.md` — the Episode 1 shot list: which scene image, what motion, what voice line, per shot.
- *(coming next, on your go)* `tts_voices.py` (Stage 1, XTTS) and `lipsync.py` (Stage 3, SadTalker/LivePortrait).

## What I can do for you right here (no GPU needed)
- Build and refine every script in this pipeline.
- Do all of Stage 4 (FFmpeg assembly, subtitles, watermark) in this box.
- Write the exact Colab notebook cells so you paste-and-run on the free GPU.
You run the GPU stages (2 and 3) on free Colab; I prep everything around them and assemble the result.
