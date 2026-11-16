#!/usr/bin/env python3
"""
JUDGEMENT TALES — Stage 2: animate one scene still into a motion clip.
Open-source Stable Video Diffusion (img2vid). Free to run on Google Colab (T4 GPU).

Install (Colab cell):
    !pip install "diffusers>=0.27" transformers accelerate imageio imageio-ffmpeg pillow

Run:
    python animate_scene.py --image images/1.jpg --out shot1.mp4 --motion 120 --fps 8

Notes
- SVD gives cinematic camera/scene motion (drift, parallax, ambient life), NOT lip-sync.
  Talking mouths are Stage 3 (SadTalker/LivePortrait) layered on top.
- Needs a GPU. On the free Colab T4 a ~4s clip renders in ~2-4 min.
- First run downloads the model (~5 GB) from Hugging Face (open weights).
"""
import argparse, torch
from PIL import Image
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import export_to_video


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="input scene still (jpg/png)")
    ap.add_argument("--out", default="shot.mp4", help="output mp4")
    ap.add_argument("--motion", type=int, default=120,
                    help="motion_bucket_id: higher = more movement (80 subtle, 180 lively)")
    ap.add_argument("--fps", type=int, default=8, help="output frames per second")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--model", default="stabilityai/stable-video-diffusion-img2vid-xt")
    args = ap.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit(
            "No CUDA GPU found. Run this on Google Colab (Runtime > T4 GPU) "
            "or a machine with an NVIDIA GPU (>=8 GB VRAM). CPU cannot render this."
        )

    dtype = torch.float16
    pipe = StableVideoDiffusionPipeline.from_pretrained(args.model, torch_dtype=dtype, variant="fp16")
    pipe.to("cuda")
    pipe.enable_model_cpu_offload()  # fits the free T4's 15 GB

    # SVD expects 1024x576. Cover-crop to keep the scene framing.
    img = Image.open(args.image).convert("RGB")
    tw, th = 1024, 576
    scale = max(tw / img.width, th / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)))
    left = (img.width - tw) // 2
    top = (img.height - th) // 2
    img = img.crop((left, top, left + tw, top + th))

    gen = torch.manual_seed(args.seed)
    frames = pipe(
        img,
        decode_chunk_size=4,
        motion_bucket_id=args.motion,
        noise_aug_strength=0.02,
        generator=gen,
    ).frames[0]

    export_to_video(frames, args.out, fps=args.fps)
    print(f"Wrote {args.out}  ({len(frames)} frames @ {args.fps}fps)")


if __name__ == "__main__":
    main()
