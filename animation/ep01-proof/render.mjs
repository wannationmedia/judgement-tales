#!/usr/bin/env node
// Judgement Tales — deterministic vector-cartoon renderer.
// Steps scene.html frame-by-frame in headless Chromium -> PNGs -> FFmpeg MP4.
// CPU-only, no GPU, no cloud. Usage: node render.mjs [fps]
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node-tools/node_modules/playwright');
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { mkdirSync, rmSync } from 'node:fs';

const DIR = dirname(fileURLToPath(import.meta.url));
const FPS = Number(process.argv[2] || 30);
const FRAMES = join(DIR, 'frames');
const OUT = join(DIR, 'the-queue-proof.mp4');

rmSync(FRAMES, { recursive: true, force: true });
mkdirSync(FRAMES, { recursive: true });

const browser = await chromium.launch({ args: ['--no-sandbox', '--force-color-profile=srgb'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
await page.goto('file://' + join(DIR, 'scene.html'));
const DUR = await page.evaluate(() => window.DUR);
const total = Math.round(DUR * FPS);
const stage = await page.$('#stage');

console.log(`Rendering ${total} frames @ ${FPS}fps (${DUR}s)...`);
for (let f = 0; f < total; f++) {
  const t = f / FPS;
  await page.evaluate((t) => window.renderAt(t), t);
  const n = String(f).padStart(5, '0');
  await stage.screenshot({ path: join(FRAMES, `f${n}.png`) });
  if (f % 30 === 0) process.stdout.write(`  frame ${f}/${total}\r`);
}
await browser.close();
console.log(`\nCaptured ${total} frames. Encoding...`);

const r = spawnSync('ffmpeg', [
  '-y', '-framerate', String(FPS),
  '-i', join(FRAMES, 'f%05d.png'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium',
  '-movflags', '+faststart', OUT
], { stdio: 'inherit' });

if (r.status !== 0) { console.error('ffmpeg failed'); process.exit(1); }
console.log(`\nDONE -> ${OUT}`);
