FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY bot/requirements.txt bot/requirements.txt
RUN pip install --no-cache-dir -r bot/requirements.txt

COPY shared/ shared/
COPY bot/ bot/

CMD ["python", "-m", "bot.main"]
