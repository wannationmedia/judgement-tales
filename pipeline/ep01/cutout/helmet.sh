#!/usr/bin/env bash
# Cartoon horned helmet, drawn to match the show's line weight. Canvas = Sven cutout coords.
STEEL='#8f979f'; STEEL_D='#69717a'; HI='#d3d8dc'; INK='#17181c'; HORN='#efe5c6'; HORN_D='#c9bb92'
convert -size 440x430 xc:none \
  -stroke "$INK" -strokewidth 5 -fill "$HORN" \
  -draw "path 'M 172,100 C 118,94 88,62 84,6 C 106,38 132,58 182,66 Z'" \
  -draw "path 'M 308,100 C 362,94 392,62 396,6 C 374,38 348,58 298,66 Z'" \
  -stroke "$HORN_D" -strokewidth 4 -fill none \
  -draw "path 'M 104,58 C 112,62 120,66 128,68'" -draw "path 'M 94,34 C 100,40 106,44 112,46'" \
  -draw "path 'M 376,58 C 368,62 360,66 352,68'" -draw "path 'M 386,34 C 380,40 374,44 368,46'" \
  -stroke "$INK" -strokewidth 6 -fill "$STEEL" \
  -draw "path 'M 150,136 C 150,22 330,22 330,136 Z'" \
  -stroke none -fill "$HI" -draw "path 'M 178,92 C 182,58 206,42 232,38 C 210,52 196,70 192,96 Z'" \
  -stroke "$INK" -strokewidth 4 -fill "$STEEL_D" -draw "rectangle 232,34 248,122" \
  -stroke "$INK" -strokewidth 6 -fill "$STEEL_D" -draw "roundrectangle 140,116 340,148 9,9" \
  -stroke none -fill "$INK" \
  -draw "circle 164,132 168,132" -draw "circle 204,132 208,132" -draw "circle 276,132 280,132" -draw "circle 316,132 320,132" \
  -draw "circle 240,52 243,52" -draw "circle 240,80 243,80" -draw "circle 240,106 243,106" \
  helmet.png
composite -compose over helmet.png sven_clean.png sven_helmet.png
convert sven_helmet.png -background '#3a7d3a' -flatten /tmp/sven_helmet_green.png
