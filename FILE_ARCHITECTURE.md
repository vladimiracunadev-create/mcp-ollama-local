# File Architecture (Mapa de Componentes)

> **Propósito:** Ofrecer un "mapa mental" instantáneo de cómo interactúan las piezas en este ecosistema (UI FastAPI → Conector Async → Sandbox de Herramientas MCP → Ollama).

Este proyecto no es monolítico, está altamente segmentado siguiendo un principio de responsabilidades separadas *(Separation of Concerns)* entre interfaz, orquestador, y ejecución segura.

## Diagrama Funcional Core

```mermaid
graph TD
    UI[Navegador/Cliente Web] -->|HTTP POST JSON| API[\apps/web/app.py/]
    API -->|Guarda Chat| DB[(data/chat_history.sqlite)]
    API -->|Llamada Async| CHAT[\host/chat_engine.py/]
    CHAT -->|Abre Sesión StdIO| BRIDGE[\host/mcp_bridge.py/]
    BRIDGE -->|Lanza Subproceso| MCPSERVER[\mcp_server/server.py/]
    CHAT -->|Petición Async LLM| OLLAMA[\host/ollama_client.py/]
    OLLAMA -->|HTTP REST| OLLAMAD[Ollama Daemon]
    OLLAMA -->|Requiere Tool| CHAT
    CHAT -->|Ejecuta Tool| MCPSERVER
    MCPSERVER -->|Lee/Escribe (Seguro)| SANDBOX[(data/sandbox/)]
```

## Exploración por Directorio

### 1. `apps/web/`
Contiene la **Capa de Presentación e Interfaz**.
- `app.py`: Servidor FastAPI de alto rendimiento (asíncrono). Expone los endpoints HTTP (`/`, `/api/chat`, `/api/health`). Recibe la solicitud del usuario web, y se apoya en el subsistema `/host` para orquestar la IA.
- `templates/` & `static/`: HTMLs (basados en CSS ligero y JS Vanilla) para interfaces ágiles, libres de frameworks pesados de frontend (ej. SPAs con React/Vue) por filosofía de minimalismo reactivo.

### 2. `host/`
Contiene la **Capa de Orquestación Lógica (El Cerebro Controlador)**.
- `chat_engine.py`: Encargado de coordinar el ritmo y las llamadas de la IA. Aquí es donde ocurre el "Bucle de Tools" (Recepción de Input → Mapeo hacia Ollama → Resolución de Función → Retorno).
- `mcp_bridge.py`: El conector *Model Context Protocol*. Convierte y "traduce" las firmas de las herramientas nativas MCP a un formato que el modelo Ollama (`host/ollama_client.py`) entienda como Functions Callings de OpenAI.
- `settings.py`: Modelo único de configuración (Pydantic). Inyecta la base direccional para Ollama y el entorno.

### 3. `mcp_server/`
Contiene la **Capa de Extensiones y Protocolo MCP**.
- `server.py`: Actúa como un *Daemmon* que FastAPI arranca bajo demanda vía un Sub-proceso estándar (`stdio`). Aquí están definidas, de forma segura usando librerías formales de Type-Hinting, herramientas como `grep_text`, `list_files`, y `system_info`.

### 4. `data/`
La **Capa Persistente Local**. Está mapeada externamente a los *volumes* de Docker/K8s.
- `chat_history.sqlite`: Almacenamiento perenne de las sesiones (id, ts, context, user).
- `sandbox/`: Carpeta enjaulada a nivel File-System por el `server.py`. Fuera de este volumen, la IA no tiene poder sobre tu máquina real.

### 5. `Infraestructura` (Raíz, K8s, GitHub)
- `pyproject.toml` y `uv.lock`: Definimos `uv` (Gestor de Dependencias Ultra-rápido en Rust). Evitamos `requirements.txt` por mutabilidad incontrolada.
- `k8s/deploy.yaml`: Manifiestos de Kubernetes para Despliegues Cloud-Native (*Liveness Probes, CPU requests*).
- `Dockerfile`: Orquestador Multi-Layer de Docker con compilación en fases y Drop de privilegios Linux (*Rootless appuser*).
