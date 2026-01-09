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

---

## Uso

Ejecuta la aplicación web:

```bash
python main.py
```

Abre tu navegador en `http://localhost:8000`.

### Endpoints
- `/`: Página principal.
- `/chat`: Interfaz de chat.
- `/options`: Ejecutar herramientas MCP.
- `/history`: Ver historial.

### API
- `POST /api/chat`: Enviar mensaje al modelo.

---

## Desarrollo

Para desarrollo local, instala dependencias con `uv`:

```bash
uv sync
```

Ejecuta tests (si existen):

```bash
uv run pytest
```

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías de contribución.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE).

---

## Seguridad

Ver [SECURITY.md](SECURITY.md) para reportar vulnerabilidades.

---

## Roadmap

Ver [ROADMAP.md](ROADMAP.md) para planes futuros.

