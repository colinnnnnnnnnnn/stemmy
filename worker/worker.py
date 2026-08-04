import logging
import time

from shared import jobs
from shared.config import OUTPUT_DIR
from worker.demucs_runner import split_stems

logger = logging.getLogger(__name__)


POLL_INTERVAL_SECONDS = 3
MODEL = "htdemucs"


def run() -> None:
    while True:
        job = _wait_for_next_job()
        _process_job(job)


def _wait_for_next_job():
    while True:
        job = jobs.claim_next_queued_job()
        if job is not None:
            return job
        time.sleep(POLL_INTERVAL_SECONDS)


def _process_job(job) -> None:
    try:
        output_path = split_stems(job.input_path, str(OUTPUT_DIR), MODEL)
        jobs.mark_job_completed(job.id, str(output_path))
    except Exception as e:
        logger.exception("Job %s failed", job.id)
        jobs.mark_job_failed(job.id, str(e))
