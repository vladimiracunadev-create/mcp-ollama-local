# 1. Fase de Construcción (Builder)
FROM python:3.13-slim as builder

# Instalar uv para gestión rápida de paquetes
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Crear el entorno virtual e instalar todas las dependencias sin las de dev
RUN uv sync --frozen --no-dev --no-install-project

# Copiar código fuente
COPY . .
# Instalar el proyecto en el venv
RUN uv sync --frozen --no-dev

# 2. Fase de Ejecución (Runner) - Imagen más ligera y segura
FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OLLAMA_URL="http://host.docker.internal:11434" \
    DATA_DIR="/app/data"

WORKDIR /app

# Copiar el entorno virtual ya construido
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

# Crear usuario rootless y asegurar permisos
RUN useradd -m appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app

# Cambiar a usuario no-root por seguridad (Rootless container)
USER appuser

EXPOSE 8000

# Usar el uvicorn del entorno virtual creado
CMD ["/app/.venv/bin/uvicorn", "apps.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
