#!/usr/bin/env bash
set -e
cd /home/user/judgement-tales/.work/build
python3 build_audio.py
python3 prepare_plates.py
python3 make_props.py
python3 render_shots.py
python3 make_subs.py
python3 assemble.py --restitch
echo "REBUILD DONE"
