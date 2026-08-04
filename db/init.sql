CREATE TABLE jobs (
  id UUID PRIMARY KEY,
  telegram_chat_id BIGINT NOT NULL,
  youtube_url TEXT NOT NULL,
  status TEXT NOT NULL, -- queued, downloading, splitting, completed, failed
  progress INTEGER NOT NULL DEFAULT 0 CHECK (progress BETWEEN 0 AND 100),
  input_path TEXT,
  output_path TEXT,
  song_title TEXT,
  error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_jobs_chat_id ON jobs (telegram_chat_id);
CREATE INDEX idx_jobs_status ON jobs (status);
CREATE INDEX idx_jobs_created_at ON jobs (created_at DESC);
