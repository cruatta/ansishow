#!/usr/bin/env bash
if [ "$(tty)" = "/dev/tty1" ]; then
 export SDL_VIDEODRIVER=fbcon
 # Run in a CW rotated framebuffer if using fbcon
 # export SDL_VIDEO_FBCON_ROTATION=CW
 exec python3 -m ansishow $HOME/art/ansi/GOAT --scaled >> /tmp/ansishow.log 2>&1
fi
