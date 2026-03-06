# Environment Setup (Entorno de Desarrollo)

Este proyecto está construido para reducir la fricción inicial ("Time to First Interaction").
Aquí detallamos los requisitos, herramientas secundarias y la configuración técnica del proyecto para contribuciones sólidas.

## Configuración de Entorno (IDE y CLI)

### 1. Variables de Entorno(`.env`)
En el archivo `host/settings.py`, consumimos estas variables estándar (que pueden o no inyectarse vía terminal o un archivo `.env`):
- `OLLAMA_URL`: Define dónde buscar el cerebro IA (`http://localhost:11434` o tu container `http://host.docker.internal:11434`).
- `MODEL`: El Target LLM a invocar (`qwen2.5-coder:7b`, `llama3`).
- `DATA_DIR`: Directorio de Data Compartida de lectura/escritura DB e historial y para el sandbox (`./data` root).

### 2. VS Code / Cursor: Plugins Recomendados
- **Ruff:** Linter oficial integrado (`charliermarsh.ruff`).
- **Mypy Type Checker:** Tipado (`ms-python.mypy-type-checker`).
- **Docker:** Para visualizar Liveness Probes de los containers (`ms-azuretools.vscode-docker`).

### 3. Setup de `uv` (Gestor de Dependencias Ultra-rápido de Python)
Usamos **`uv`** escrito en Rust para la gestión de lockfiles (`uv.lock`) en vez de Pip puro.
- **Para arrancar local**: Correr `make install` el cual llamará a `uv sync` construyendo un `.venv` idéntico bit-a-bit.

## Configuración Especial: Model Context Protocol (MCP) C++ / Rust
Si añades tools más densas de sistema, asegúrate de utilizar el package nativo `mcp` que hemos seteado el cual levanta subprocesos de lectura usando standard IO (`stdio`).
