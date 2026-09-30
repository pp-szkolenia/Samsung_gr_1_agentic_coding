FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.10 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1

COPY simple_server simple_server

EXPOSE 8030
CMD ["watchfiles", "python -m simple_server.main", "simple_server"]