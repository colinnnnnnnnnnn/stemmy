FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY worker/requirements.txt worker/requirements.txt
RUN uv pip install --no-cache-dir -r worker/requirements.txt

COPY shared/ shared/
COPY worker/ worker/

CMD ["python", "-m", "worker.main"]
