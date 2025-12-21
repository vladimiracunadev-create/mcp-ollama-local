# mcp-ollama-local

Web local (FastAPI) + IA local (Ollama) + Tools vía MCP.  
Proyecto pensado para correr en un Mac (en disco externo ORICO) y conversar con un modelo local de texto, con acceso seguro a herramientas (system_info/list_files/grep_text) y con historial en SQLite.

## Qué es esto (en simple)

- **/chat**: Chat conversacional (tú escribes, el modelo responde).
- **/options**: Ejecuta tools MCP directo (sin IA).
- **/history**: Muestra historial guardado en SQLite (si activaste esa vista).

Pipeline:
Navegador → FastAPI (`/api/chat`) → Ollama (modelo) → (si aplica) MCP tools → respuesta en pantalla.

---

## Requisitos

1) **Ollama** instalado y corriendo (local)
2) Python en entorno virtual del proyecto (ya estás usando `.venv` con `uv`)
3) Modelo descargado en Ollama (ej. `qwen3:8b`)

---

## Instalación rápida

Desde la raíz del proyecto:

```bash
# 1) activar venv (si aplica)
source .venv/bin/activate

# 2) verificar ollama
ollama --version
ollama list

# 3) descargar un modelo (ejemplo)
ollama pull qwen3:8b

