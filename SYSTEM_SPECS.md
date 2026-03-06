# Especificaciones del Sistema y Servidor

Para correr LLMs locales que además interactúan como "Agentes" (consumiendo herramientas de Model Context Protocol de Python Subprocess de manera asincrónica), los sistemas demandan características concretas.

## 1. Hardware Mínimo Esperable (Bare-Metal/Laptop)

- **CPU:** Apple Silicon (M1/M2/M3 Base) o procesador con instrucciones AVX2 (Intel Core de 8.va Gen o superior / Ryzen Base).
- **RAM (Motor LLM):** Mínimo **8 GB netos** para los modelos ágiles y fuertemente cuantizados de codificación (Ej. `qwen2.5-coder:7b`).
- **RAM (App FastAPI):** ~150 MB (Micro-footprint local).

## 2. Docker Engine (Para Host.Docker.Internal)

- **Mac / Win WSL2:** La ruta `http://host.docker.internal:11434` funciona como puente directo al puerto del Localhost exterior.
- **Linux Puro:** Docker debe iniciarse indicando explícitamente habilitación de `host-gateway`, como se configuró en `docker-compose.yml`.

## 3. Kubernetes Specs (Requests vs Limits)

El archivo `k8s/deploy.yaml` define las siguientes cuotas estrictas de recursos para el POD de FastAPI:

* **Requests (Mínimo reservado):** 250m CPU / 256Mi RAM.
* **Limits (Tope estricto de freno - OOMKilled):** 500m CPU / 512Mi RAM.

*(Nota: En escenarios empresariales reales, Ollama se sirve en un Pool o Nodo de GPUs separado o bajo NVIDIA Triton. Los Limits expuestos aquí son exclusivamente para proteger el frontend y el conector API Async que no consume VRAM).*
