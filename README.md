# Stemmy – Audio Processing & Stem Separation Pipeline

A backend service that separates audio into individual instrument stems through Telegram. Users send a YouTube URL to the Telegram bot, Stemmy downloads the audio using yt-dlp, separates it using Demucs, and sends the resulting stems back as audio files.

Stemmy is designed as a backend-focused project, with an emphasis on persistent job management, background processing, service separation, and containerized deployment.

## Features

* **YouTube Audio Processing** — Downloads and converts audio using yt-dlp and FFmpeg
* **Stem Separation** — Uses Demucs to separate audio into vocals, drums, bass, and other
* **Persistent Job Tracking** — PostgreSQL stores job state, metadata, and results
* **Background Processing** — Dedicated worker service handles long-running audio processing
* **Service Separation** — Telegram bot and processing worker operate independently
* **Docker Deployment** — Reproducible, self-hosted deployment using Docker Compose

## Architecture

```text
User
 │
 ▼
Telegram Bot
 │
 ▼
PostgreSQL
 │
 ▼
Worker
 │
 ▼
Demucs
 │
 ▼
Filesystem
 │
 ▼
Telegram Bot
 │
 ▼
User
```

The Telegram bot handles user interaction and audio downloads, while a separate worker processes queued jobs using Demucs. PostgreSQL acts as the shared source of truth for job state and coordinates the two services.

## Processing Flow

1. User sends a YouTube URL through Telegram
2. Bot creates a job and downloads the audio using yt-dlp
3. Job is added to the PostgreSQL queue
4. Worker claims a queued job using an atomic database update
5. Demucs separates the audio into four stems
6. Worker stores the results and marks the job as completed
7. Bot detects completion and sends the stems back to the user

Jobs transition through the following states:

```text
downloading → queued → splitting → completed
            ↘ failed             ↘ failed
```

## Technology Stack

| Technology          | Purpose                                    |
| ------------------- | ------------------------------------------ |
| Python              | Application logic                          |
| PostgreSQL          | Persistent job and state storage           |
| Docker Compose      | Containerization and service orchestration |
| yt-dlp              | YouTube audio retrieval                    |
| FFmpeg              | Audio conversion                           |
| Demucs              | Neural network-based stem separation       |
| psycopg             | PostgreSQL driver and connection pooling   |
| python-telegram-bot | Telegram Bot API client                    |

## Design Highlights

**PostgreSQL-backed job queue**

Jobs are persisted in PostgreSQL rather than relying on filesystem or in-memory state. This gives the application persistent job state and allows the bot and worker to coordinate through a shared source of truth.

**Separate bot and worker services**

The Telegram bot is responsible for user interaction and downloading, while a dedicated worker performs the CPU-intensive Demucs processing. This keeps long-running processing separate from the user-facing service.

**Atomic job claiming**

Workers claim queued jobs through an atomic database update, preventing multiple workers from processing the same job simultaneously.

**Subprocess-based processing**

yt-dlp and Demucs are invoked as external processes rather than being tightly coupled to the application logic. This keeps the audio-processing tools isolated and simplifies dependency management.

**Containerized deployment**

The bot, worker, and PostgreSQL database run as separate Docker services managed through Docker Compose, allowing the complete application to be deployed consistently on a self-hosted server.

## Running Locally

### Prerequisites

* Docker and Docker Compose
* A Telegram bot token from [@BotFather](https://t.me/botfather)

### Quick Start

```bash
git clone https://github.com/colinnnnnnnnnnn/stemmy.git
cd stemmy

cp .env.example .env
```

Edit `.env` and provide your Telegram bot token, then start the services:

```bash
docker compose up -d
```

View the application logs with:

```bash
docker compose logs -f bot
docker compose logs -f worker
```

Send a YouTube URL to the bot to start processing.

To stop the application:

```bash
docker compose down
```

## Deployment

Stemmy is designed for self-hosted deployment using Docker Compose.

PostgreSQL data is persisted through a Docker volume, while downloaded and processed audio is stored in the configured data directories.

## Project Structure

```text
stemmy/
├── bot/                   # Telegram bot service
│   ├── main.py
│   ├── handlers.py
│   ├── workflow.py
│   ├── downloader.py
│   ├── Dockerfile
│   └── requirements.txt
├── worker/                # Audio processing worker
│   ├── main.py
│   ├── worker.py
│   ├── demucs_runner.py
│   ├── Dockerfile
│   └── requirements.txt
├── shared/                # Shared database and application code
│   ├── config.py
│   ├── db.py
│   ├── jobs.py
│   ├── models.py
│   └── exceptions.py
├── db/
│   └── init.sql           # Database schema
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

## Future Improvements

* **Multiple workers** — Run multiple worker instances to process jobs concurrently
* **Message queue** — Replace database polling with a dedicated message queue
* **Object storage** — Store audio files using S3-compatible storage such as MinIO
* **Automatic retries** — Retry failed jobs with exponential backoff
* **Monitoring & metrics** — Add Prometheus metrics and service monitoring
* **Rate limiting & authentication** — Restrict usage and prevent abuse
