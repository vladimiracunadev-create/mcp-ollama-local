# Prácticas y Herramientas "Killed" ☠️

Como Arquitecto, a veces "qué **no** usar" es una decisión mucho más clave que "qué sumar a la fuerza".
Esta es la lista de anti-patrones, tecnologías y decisiones que veté conscientemente para `mcp-ollama-local` y el por qué.

### 1. ☠️ Bases de Datos Complejas (Postgres/MySQL para Chat)
- **Motivo del Veto:** Es un overkill injustificado. Este proyecto gestiona historias de chat 1 a 1 de agente local, la persistencia no requiere ACID complejo distribuido inicial, ni balanceo en réplicas read/write transaccionales pesadas para su core.
- **Qué se usa en vez:** Base de datos relacional ligera *SQLite* (Persistent Volume-Attached en contenedores de Kubernetes con claims). Funcional, rápido, portable.

### 2. ☠️ Single Page Applications (React/Vue/Angular)
- **Motivo del Veto:** Este repositorio persigue demostrar simplicidad orquestada por Python y un LLM. Elevar una SPA para leer un texto JSON de IA requeriría un *build-step* con Node.js, empantanando el `Dockerfile` y violando el principio minimalista de Fast-Loading.
- **Qué se usa en vez:** Server-Side Rendering mediante `FastAPI HTMLResponse` e indexación minimalista (archivos estáticos Vanilla JS/CSS). 

### 3. ☠️ Ejecución Root de Contenedores Docker (Supervisores Privilegiados)
- **Motivo del Veto:** Inseguro en extremo tratándose de un servidor *MCP* expuesto a IA autónoma local. Si Ollama lograse inyectar comandos perjudiciales a través del MCP Subprocess en el *Sandbox*, al usar un Root se arriesga a comprometer el host que hospeda el daemon.
- **Qué se usa en vez:** Contenedor *Rootless* desde compilación. Un usuario restrictivo *No Privilegiado* (`appuser`).

### 4. ☠️ Scripts Bash "A mano" sin Liveness/Safety Checks
- **Motivo del Veto:** Un script suelto sin test de falla es la fuente clásica del "mantenimiento pesado oculto".
- **Qué se usa en vez:** Validaciones con CI en GitHub. *Bandit* automatizado en Actions para descubrir inyecciones y validaciones con *Ruff*. Flujo con un Makefile automatizado base (`make *`).

### 5. ☠️ Dependencias Ad-hoc via `pip` y Hard-coding Tools
- **Motivo del Veto:** Fricción dev-ops paralizante y configuraciones bloqueadas a código quemado en un framework oscuro que requiera modificar todo el programa si se inventa una herramienta nueva.
- **Qué se usa en vez:** Model Context Protocol (Desacoplamiento Funcional Nivel Anthropic) vía `mcp_server`. Gestor *rust-based* dependencias con `uv` y manifiestos absolutos `.lock`.
