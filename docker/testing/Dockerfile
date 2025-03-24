FROM python:3.13-slim

ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_PYTHON_DOWNLOADS=never

COPY --from=ghcr.io/astral-sh/uv:0.6.9 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

COPY docker/testing/startup.sh .
RUN chmod +x startup.sh

RUN uv sync --frozen --no-install-project
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

CMD ["./startup.sh"]
