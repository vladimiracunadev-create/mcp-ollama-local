# Usar una imagen base ligera de Python
FROM python:3.13-slim

# Instalar uv para gestión rápida de paquetes
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    App_DIR=/app

WORKDIR $App_DIR

# Instalar dependencias del sistema mínimas (si fueran necesarias)
# RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Copiar archivos de definición de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias usando uv
RUN uv sync --frozen --no-dev --no-install-project

# Copiar el código de la aplicación
COPY . .

# Instalar el proyecto en sí
RUN uv sync --frozen --no-dev

# Crear usuario no-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Variables de entorno por defecto (pueden sobreescribirse)
ENV OLLAMA_URL="http://host.docker.internal:11434"
ENV DATA_DIR="/app/data"

# Ejecutar la aplicación
CMD ["uv", "run", "uvicorn", "apps.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
