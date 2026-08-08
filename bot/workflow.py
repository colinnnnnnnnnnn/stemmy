import asyncio
import logging
from pathlib import Path

from bot.downloader import download_audio
from shared import jobs
from shared.config import INPUT_DIR
from shared.exceptions import DownloadError, JobFailedError

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 2


async def process_youtube_url(chat_id: int, url: str) -> Path:
    job_id = jobs.create_job_from_url(chat_id, url)
    logger.info("Job %s: created for chat %s", job_id, chat_id)

    try:
        logger.info("Job %s: downloading from URL %s", job_id, url)
        input_path = await _download_to_input_dir(url, job_id)
        logger.info("Job %s: download success", job_id)
    except Exception as e:
        logger.exception("Job %s: download failed.", job_id)
        jobs.mark_job_failed(job_id, error=str(e))
        raise DownloadError(f"Failed to download for job {job_id}") from e

    song_title = input_path.stem
    jobs.update_job_song_title(job_id, song_title)
    jobs.mark_job_queued(job_id, input_path=str(input_path))
    logger.info("Job %s: queued for splitting. Title: '%s'", job_id, song_title)

    job = await _wait_for_completion(job_id)

    if job.status == "failed":
        raise JobFailedError(job.error or "Unknown worker error")

    if job.output_path is None:
        raise JobFailedError(f"Job {job_id} completed but has no output path")

    logger.info("Job %s: successfully processed", job_id)
    return Path(job.output_path)


async def _download_to_input_dir(url: str, file_name: str) -> Path:
    loop = asyncio.get_running_loop()
    # download_audio is blocking (subprocess) — keep it off the event loop
    path = await loop.run_in_executor(
        None, download_audio, url, str(INPUT_DIR), file_name
    )
    return path


async def _wait_for_completion(job_id: str):
    while True:
        job = jobs.get_job(job_id)
        if job.status in ("completed", "failed"):
            return job
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
