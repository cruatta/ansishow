#!/usr/bin/env bash
# Run in a CCW rotated framebuffer
export SDL_VIDEO_FBCON_ROTATION=CCW
exec python3 $HOME/ansishow/ansishow $HOME/art/ansi/GOAT --scaled >> /tmp/ansishow.log 2>&1