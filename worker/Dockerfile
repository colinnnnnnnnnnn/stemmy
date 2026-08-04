FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN uv --version
# create venv
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY worker/requirements.txt worker/requirements.txt
RUN uv pip install --no-cache-dir -r worker/requirements.txt

COPY shared/ shared/
COPY worker/ worker/

ENTRYPOINT ["/bin/sh", "/demucs-watch.sh"]
