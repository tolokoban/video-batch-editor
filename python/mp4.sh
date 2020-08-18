#!/usr/bin/env bash

ffmpeg -y -framerate 30 -i /gpfs/bbp.cscs.ch/project/proj3/tolokoban/SSCx/input/final/%05d.jpg -c:v libx264 -crf 23 -profile:v high -pix_fmt yuv420p -color_primaries 1 -color_trc 1 -colorspace 1 -movflags +faststart -an ./output.mp4
