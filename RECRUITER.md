# 👔 RECRUITER (Logros de Ingeniería)

> [!TIP]
> Este documento responde a la pregunta de Técnicos, Headhunters y Engineering Managers: **"¿Por qué este repo es relevante entre los millones creados con IA, y qué habilidades tangibles demuestra este desarrollador?"**.

## El "Pitch" Ejecutivo
`mcp-ollama-local` no es otro tutorial más de "cómo hacer llamadas en Python a OpenAI". Es una **arquitectura de infraestructura en la sombra (shadow-infra), asíncrona, orientada hacia Kubernetes y con filosofía de Seguridad Primero.**

Este proyecto conjuga en un mismo pipeline: IA generativa 100% privada (Ollama en Bare-Metal Local/Intranet) enlazada robustamente al emergente diseño de **Model Context Protocol** (herramientas locales nativas seguras); estructurada funcionalmente bajo **FastAPI** asíncrono y empaquetada estrictamente bajo los más duros estándares **DevOps y SRE**.

## 🛠 Qué Habilidades Específicas se Demuestran Aquí

### 1. Delivery Orientado a Cloud y K8s-First
No basta con que el script funcione local. Demuestro la capacidad de llevar una idea experimental a producción:
- **`Dockerfile` Multi-Stage de grado Security-Team:** Construcción compilada donde se descargan variables en un contenedor `builder`, traspasando solo el resultado limpio reduciendo el footprint dramáticamente en Megabytes.
- **Rootless Containers by default:** Transición obligatoria a un usuario sin privilegios `appuser`.
- **Manifiestos K8s Industriales:** `k8s/deploy.yaml` posee recursos estrictos (limits/requests CPU de 250m) para evitar *Denial of Application* en clusters saturados, y probes automatizadas de vida HTTP (`livenessProbe`) nativas atacando la ruta construida en FastAPI (`/api/health`).

### 2. CI/CD: "Quality Gates" Estrictos y Comprobables
La carpeta `.github/workflows` define mi acercamiento inamovible para equipos distribuidos (CI/CD Automático):
- **Bandit (Sec-Ops):** Análisis forzado contra inyección y vulnerabilidades en código. Se resolvieron proactivamente vectores de inyección SQL (B608) mediante refactorización de consultas parametrizadas.
- **Pip-Audit:** Monitoreo constante de vulnerabilidades en la cadena de suministro de dependencias (CVEs), asegurando que el proyecto corra sobre librerías parchadas y seguras.
- **Ruff (Linter y Format):** Asegura cumplimiento estricto de Guías Pep-8 a 88 lineas.
- **Pytest/Cov:** Evaluaciones forzadas que interrumpen integraciones si caen los tests e-2-e locales (de FastApi) implementados para evitar regresiones de interfaz.

### 4. Seguridad en 8 Capas (Defense in Depth)
He transformado una herramienta local en una aplicación con controles concretos y verificables:
1. **Container Hardening**: Rootless, Healthchecks y pinning de imágenes.
2. **Network Isolation**: Localhost-only binding por defecto.
3. **App Security**: Middlewares de headers, HSTS condicional bajo HTTPS y Rate Limiting simple.
4. **Auth Layer**: Soporte nativo para API_KEY obligatoria.
5. **Tool Sandbox**: Validación estricta de rutas MCP y enmascaramiento de OS.
6. **SAST/Audit**: Integración de Bandit y auditoría de dependencias en CI.

### 3. Observabilidad, Mantenibilidad y DX de Herramientas Rápidas
- Fuerte orientación al **Developer Experience (DX)** usando la reciente y veloz librería **`uv` de Astral** (Rust-based environment) para resolver el ecosistema Python, huyendo de las arcaicas instalaciones eternas de dependencias y mutabilidad (*lockfiles* absolutos).
- Simplificación manual con herramientas como `Makefile` local que normaliza operaciones complejas de testing de QA local con un comando ciego (`make run`).
- Componentes altamente acoplados internamente pero desacoplados a nivel API (File-System Sandbox que no muta o corrompe por agentes de IA autónoma).

## 🚀 Valor Adicional para tu Equipo
* "Conocimiento del Estado del Arte": El uso nativo del protocolo MCP en sus primeros albores de popularidad para extender las alas de agentes sin la traba de configuraciones en hardcode en Python. Incorporo innovaciones con bases resilientes tradicionales en mente.
* Mis proyectos son reproducibles; no dependen del "en mi máquina funciona".

Puntualmente busco **Sistemas Desafiantes, Arquitecturas de Solución o Roles Bridge Technical Lead/Operations**.

---

### 📚 Documentación Relacionada
- [README.md](README.md) | [FILE_ARCHITECTURE.md](FILE_ARCHITECTURE.md) | [SYSTEM_SPECS.md](SYSTEM_SPECS.md)
