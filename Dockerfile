FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock README.md ./
COPY src/ src/
COPY data/ data/

RUN uv sync --no-dev --extra api --frozen

ENV PORT=8000
EXPOSE ${PORT}

CMD uv run booklib serve --host 0.0.0.0 --port ${PORT}
