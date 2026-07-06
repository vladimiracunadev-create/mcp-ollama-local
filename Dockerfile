# 1. Fase de Construcción (Builder)
FROM python:3.13-slim@sha256:eb43ff125d8d58d7449dcba7d336c23bcac412f526d861db493b9994d8010280 AS builder

# Instalar uv para gestión rápida de paquetes (Versión fija)
COPY --from=ghcr.io/astral-sh/uv:0.5.21 /uv /bin/uv

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
FROM python:3.13-slim-bookworm@sha256:fcbd8dfc2605ba7c2eca646846c5e892b2931e41f6227985154a596f26ab8ed7

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
    && chown -R appuser:appuser /app/data \
    && chmod -R 755 /app \
    && chmod -R 777 /app/data

# Cambiar a usuario no-root por seguridad
# Instalar curl para el healthcheck (opcional pero recomendado)
# RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# Healthcheck usando python para no añadir dependencias extras
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/app/.venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"]

EXPOSE 8000

# Usar el uvicorn del entorno virtual creado
CMD ["/app/.venv/bin/uvicorn", "apps.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
