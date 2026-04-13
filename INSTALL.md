# 📦 Instalación y Quickstart

> [!TIP]
> Si quieres la ruta más directa para probar el proyecto, empieza por local o Docker y valida con `/api/health` antes de depurar la UI.

## 📋 Requisitos

- Python 3.13
- `uv`
- Ollama instalado y corriendo
- Un modelo descargado, por ejemplo `qwen3:8b`

## 💻 Opción 1: local

```bash
git clone https://github.com/vladimiracunadev-create/mcp-ollama-local.git
cd mcp-ollama-local
uv sync --frozen
ollama pull qwen3:8b
make run
```

Abrir:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

## ⚙️ Configuración opcional

Crea `.env` si necesitas cambiar modelo, URL o protección por API key:

```bash
MODEL=qwen3:8b
OLLAMA_URL=http://localhost:11434
DATA_DIR=./data
# API_KEY=change-me
# REQUIRE_API_KEY=false
# ALLOWED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
```

## 🐳 Opción 2: Docker

```bash
docker compose up --build
```

Características reales del despliegue:

- proceso no-root,
- persistencia montada en `./data`,
- publish en `127.0.0.1:8000`,
- healthcheck HTTP local.

Consideraciones:

- En Mac/Windows, `host.docker.internal` suele funcionar de forma directa.
- En Linux, revisa soporte `host-gateway` y el bind de Ollama.
- Si Ollama escucha solo en `127.0.0.1`, el contenedor puede no alcanzarlo.

## ☸️ Opción 3: Kubernetes

Los manifiestos incluidos son básicos y útiles para laboratorio, no una distribución de producción.

```bash
docker build -t mcp-ollama-local:latest .
kubectl apply -f k8s/deploy.yaml
kubectl apply -f k8s/service.yaml
kubectl port-forward svc/mcp-ollama-service 8080:80
```

Notas:

- El `PersistentVolumeClaim` es simple y asume un `StorageClass` funcional.
- `OLLAMA_URL` en `k8s/deploy.yaml` debe ajustarse a tu topología real.

## ✅ Validación posterior a la instalación

```bash
make lint
make test
make audit
curl -sS http://127.0.0.1:8000/api/health
```

## 🔧 Troubleshooting corto

- Si `make run` arranca pero el chat falla, consulta `/api/health`.
- Si Docker responde pero `ollama_ok=false`, revisa conectividad hacia `host.docker.internal:11434`.
- Si activas `REQUIRE_API_KEY=true`, recuerda enviar `X-API-Key`.

Más detalles en [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
