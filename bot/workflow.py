import asyncio

# import logging
from pathlib import Path

from bot.downloader import download_audio
from shared import jobs
from shared.exceptions import DownloadError, JobFailedError

# logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 2


async def process_youtube_url(chat_id: int, url: str) -> Path:
    job_id = jobs.create_job_from_url(chat_id, url)

    try:
        jobs.mark_job_downloading(job_id)
        input_path = await _download_to_input_dir(url)
    except Exception as e:
        jobs.mark_job_failed(job_id, error=str(e))
        raise DownloadError(f"Failed to download for job {job_id}") from e

    song_title = input_path.stem
    jobs.update_job_song_title(job_id, song_title)
    jobs.mark_job_queued(job_id, input_path=str(input_path))

    job = await _wait_for_completion(job_id)

    if job.status == "failed":
        raise JobFailedError(job.error or "Unknown worker error")

    return Path(job.output_path)


async def _download_to_input_dir(url: str) -> Path:
    loop = asyncio.get_running_loop()
    # download_audio is blocking (subprocess) — keep it off the event loop
    path = await loop.run_in_executor(None, download_audio, url, str(INPUT_DIR))
    return path


async def _wait_for_completion(job_id: str):
    while True:
        job = jobs.get_job(job_id)
        if job.status in ("completed", "failed"):
            return job
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
