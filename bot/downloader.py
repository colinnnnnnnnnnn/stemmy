import os
import subprocess
from pathlib import Path


def download_audio(url: str, input_dir: str, job_id: str) -> Path:
    job_dir = Path(input_dir) / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

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
                os.path.join(job_dir, "%(title)s.%(ext)s"),
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
