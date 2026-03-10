FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY src/ src/
COPY data/ data/

RUN uv sync --no-dev --extra api --frozen

EXPOSE 8000

CMD ["uv", "run", "booklib", "serve", "--host", "0.0.0.0", "--port", "8000"]
