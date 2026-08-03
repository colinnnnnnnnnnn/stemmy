import os
import subprocess
from pathlib import Path


def download_audio(url: str, download_path: str) -> Path:
    try:
        res = subprocess.run(
            [
                "yt-dlp",
                "--extract-audio",
                "--audio-format",
                "mp3",
                "--print",
                "after_move:filepath",
                "-o",
                os.path.join(download_path, "%(title)s.%(ext)s"),
                url,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        res_path = Path(res.stdout.strip().splitlines()[-1])
        return res_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"yt-dlp failed: {e.stderr}")
