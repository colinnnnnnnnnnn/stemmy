#!/bin/sh
set -eu
echo "Demucs watcher started"
ls -la /data
ls -la /data/input || true
mkdir -p /data/input /data/output /data/done

while true; do
  for f in /data/input/*.mp3; do
    [ -f "$f" ] || continue
    echo "Processing $f"
    demucs -n htdemucs -o /data/output "$f" && mv "$f" /data/done/
  done
  sleep 3
done
