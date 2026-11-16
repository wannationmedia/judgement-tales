# Episode 1 "The Queue" — shot list for the pipeline

You currently have **5 scene stills**. A full 10-min episode needs **one still per shot** (dozens). Those extra stills are **Stage 0**: generate more frames in the same cartoon style from the script, using open-source **SDXL or FLUX** (free on Colab) with a style reference from your existing art. Then each still → Stage 2 motion → Stage 3 talking → Stage 4 assemble.

## Starter shots from your existing 5 stills (prove the look moves first)
| Shot | Source still | Stage-2 motion | Voice line (Stage 1 TTS) | Character voice |
|---|---|---|---|---|
| 1 | images/1.jpg (Reception) | slow push-in, crowd drift; `--motion 110` | "Take a ticket. Zero-four-seven." | St. Peter — fussy old-world |
| 2 | images/1.jpg (Reception, Lwazi) | subtle head/hand motion; `--motion 90` | "Sharp. Okay. I'm not even mad." | Lwazi — Joburg SA |
| 3 | images/4.jpg (Sultan/elevator) | robe sway, gesture; `--motion 130` | "The Sultan does not queue. The Sultan visits." | The Sultan — grand Levantine |
| 4 | images/3.jpg (Complaints) | paper flutter, Moses sigh; `--motion 100` | "Complaint number one. Water. I have heard this one before." | Moses — weary Persian |
| 5 | images/2.jpg (Orientation) | Jesus presenting, slide glow; `--motion 110` | "Great question. Let's park it." | Jesus — measured trainer |
| 6 | images/5.jpg (Boardroom) | chart shimmer, nods; `--motion 95` | "Just rename Pending to In Transition." | Angel analyst |

## Per-shot command (free Colab GPU)
```bash
python animate_scene.py --image images/1.jpg --out shot1.mp4 --motion 110 --fps 8
```
Repeat per row, then list them in `shots.txt` and run `assemble.sh`.

## Honest effort estimate (free, but real work)
- Stage 0 (make all the stills): the biggest lift — one good image per shot, consistent characters. A style LoRA trained on your 5 frames keeps everyone on-model.
- A tight **2–3 min animated short** of Ep 1's best beats is a realistic first real deliverable. The full 10-min pilot is that, scaled up.
- All free on Colab/your GPU. The only cost is GPU time (free tiers) and iteration.
