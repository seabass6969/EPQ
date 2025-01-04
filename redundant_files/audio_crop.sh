#!/bin/sh
ffmpeg -ss 0 -i input.wav -t 10 -c:a copy mono.wav