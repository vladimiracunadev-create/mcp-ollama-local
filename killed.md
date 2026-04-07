# ☠️ Prácticas y Herramientas "Killed"

> [!NOTE]
> Como Arquitecto, a veces "qué **no** usar" es una decisión mucho más clave que "qué sumar a la fuerza".
> Esta es la lista de anti-patrones, tecnologías y decisiones que veté conscientemente para `mcp-ollama-local`.

### 1. 🛑 Bases de Datos Complejas (Postgres/MySQL)
- **Motivo del Veto:** Es un overkill injustificado para chat local.
- **Qué se usa en vez:** *SQLite* (Rápido, portable, zero-config).

### 2. 🛑 SPA Pesadas (React/Vue/Angular)
- **Motivo del Veto:** Este repositorio busca simplicidad absoluta. Evitamos pasos extra de compilación (Node.js/npm) en el contenedor.
- **Qué se usa en vez:** Server-Side Rendering mediante `FastAPI` y Vanilla JS.

### 3. 🛑 Ejecución Root en Docker
- **Motivo del Veto:** Inseguro. Un escape de sandbox con privilegios de root comprometería todo el host.
- **Qué se usa en vez:** Contenedor *Rootless* con `appuser`.

### 4. 🛑 Scripts Bash "Manuales"
- **Motivo del Veto:** Fuente de errores silentes y pesadilla de mantenimiento.
- **Qué se usa en vez:** Automatización vía `Makefile` y validaciones en CI/CD con **Bandit**.

---

### 📚 Documentación Relacionada
- [README.md](README.md) | [RECRUITER.md](RECRUITER.md) | [GLOSSARY.md](GLOSSARY.md)
