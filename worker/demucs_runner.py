import subprocess
from pathlib import Path


def split_stems(input_path: str, output_dir: str, model: str, job_id: str) -> Path:
    try:
        res = subprocess.run(  # res to be used later for capturing progress
            [
                "demucs",
                "-n",
                model,
                "--mp3",
                "--filename",
                f"{job_id}/{{stem}}.{{ext}}",
                "-o",
                output_dir,
                input_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"demucs failed: {e.stderr}")

    # Precompute output path deterministically (demucs has no flag to print output path)
    output_path = Path(output_dir) / model / str(job_id)

    if not output_path.exists():
        raise RuntimeError(
            f"Expected demucs output at {output_path}, but it wasn't found"
        )

    return output_path
