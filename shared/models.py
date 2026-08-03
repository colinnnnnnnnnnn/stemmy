from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    id: str
    telegram_chat_id: int
    youtube_url: str
    status: str
    progress: int
    input_path: str | None
    output_path: str | None
    error: str | None
    song_title: str | None
    created_at: datetime
    updated_at: datetime
