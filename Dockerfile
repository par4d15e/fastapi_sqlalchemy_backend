# ======= runtime-focused Dockerfile =======
# use slim base and avoid dev-only packages/user setup
FROM python:3.14-slim

# keep python output unbuffered for logs and set a working dir
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# copy project metadata first so dependency installation can be cached
COPY pyproject.toml README.md ./

# install build requirements and project dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir .

# copy application code
COPY app ./app
COPY alembic ./alembic

# expose port for uvicorn (optional)
EXPOSE 8000

# default command to run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

