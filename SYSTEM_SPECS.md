# 📊 Especificaciones del Sistema y Servidor

> [!NOTE]
> Para correr LLMs locales que además interactúan como "Agentes" (consumiendo herramientas de Model Context Protocol de Python Subprocess de manera asincrónica), los sistemas demandan características concretas.

## 1. Hardware Mínimo Esperable (Bare-Metal/Laptop)

- **CPU:** Apple Silicon (M1/M2/M3 Base) o procesador con instrucciones AVX2 (Intel Core de 8.va Gen o superior / Ryzen Base).
- **RAM (Motor LLM):** Mínimo **8 GB netos** para modelos ligeros o cuantizados (Ej. `qwen3:8b`).
- **RAM (App FastAPI):** ~150 MB (Micro-footprint local).

## 2. Docker Engine (Para Host.Docker.Internal)

- **Mac / Win WSL2:** La ruta `http://host.docker.internal:11434` funciona como puente directo al puerto del Localhost exterior.
- **Linux Puro:** Docker debe iniciarse indicando explícitamente habilitación de `host-gateway`, como se configuró en `docker-compose.yml`.

## 3. Kubernetes Specs (Requests vs Limits)

El archivo `k8s/deploy.yaml` define las siguientes cuotas estrictas de recursos para el POD de FastAPI:

* **Requests (Mínimo reservado):** 250m CPU / 256Mi RAM.
* **Limits (Tope estricto de freno - OOMKilled):** 500m CPU / 512Mi RAM.

*(Nota: En escenarios empresariales reales, Ollama se sirve en un Pool o Nodo de GPUs separado o bajo NVIDIA Triton. Los Limits expuestos aquí son exclusivamente para proteger el frontend y el conector API Async que no consume VRAM).*

## 4. Seguridad Integrada (Defense in Depth)

El sistema opera bajo un modelo de **Defensa en Profundidad** para entornos locales y productivos:
1. **Contenedor**: Usuario no-root (`appuser`), puerto 8000, `HEALTHCHECK` activo.
2. **Red**: Bind exclusivo a `127.0.0.1` en Compose para evitar exposición en red LAN.
3. **App Web**: Middlewares de Cabeceras de Seguridad y Rate Limiting (60 req/min).
4. **Auth**: Capa `X-API-Key` opcional u obligatoria según `.env`.
5. **MCP**: Validación estricta de rutas y sandbox enjaulado en `data/sandbox`.

---

### 📚 Documentación Relacionada
- [README.md](README.md) | [FILE_ARCHITECTURE.md](FILE_ARCHITECTURE.md) | [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
