# 📜 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [0.2.0] - 2026-04-06

### Añadido
- **Seguridad (Hardening en 8 Capas)**: Implementación de arquitectura "Defense in Depth":
    - **Capa 1 (Contenedor)**: Usuario `appuser` (no-root), `HEALTHCHECK` local y tags de imagen fijos.
    - **Capa 2 (Red)**: Binding de puertos a `127.0.0.1` en Docker Compose para prevenir exposición en LAN.
    - **Capa 3 (Credenciales)**: Soporte para `API_KEY` y modo obligatorio `REQUIRE_API_KEY`.
    - **Capa 4 (Web)**: Middlewares para cabeceras de seguridad (`CSP`, `HSTS`, `Referrer`, `Permissions`) y Rate Limiting (60 req/min).
    - **Capa 5 (MCP)**: Sandbox reforzado con validación de rutas y enmascaramiento de info del sistema host.
    - **Capa 6 (Auth)**: Validación `X-API-Key` en todos los puntos de entrada de la API.
    - **Capa 7 (CI/CD)**: Workflow `security.yml` para escaneo de vulnerabilidades y linting en cada push.
    - **Capa 8 (Supply Chain)**: Configuración de `.gitattributes` para forzar finales de línea `LF`.

### Corregido
- **API**: Corregido bug en `/api/history` que pasaba parámetros duplicados a SQLite.
- **Herramientas**: `system_info` ya no filtra rutas absolutas del servidor host.

## [0.1.1] - 2026-03-06

### Cambiado
- **Docker**: `Dockerfile` reescrito usando arquitectura Multi-Stage para reducir drásticamente el tamaño final de la imagen, e implementada ejecución de contenedor en modo *Rootless* (usuario `appuser`) maximizando la seguridad.
- **Kubernetes**: Manifiesto de despliegue (`k8s/deploy.yaml`) robustecido. Incluye ahora *Liveness Probes*, *Readiness Probes* (consumiendo `/api/health`), y cuotas de recursos estrictas (*Limits/Requests*).
- **CI/CD**: Pipeline de GitHub Actions expandido para integrar reporte de cobertura y validaciones de seguridad por cada commit.

## [0.1.0] - 2026-01-22### Añadido
- **Infraestructura**: Soporte completo para Docker (`Dockerfile`, `docker-compose.yml`) y Kubernetes (`k8s/`).
- **CI/CD**: Workflow de GitHub Actions para linting, formateo y testing automático.
- **Automatización**: Nuevo `Makefile` para estandarizar comandos (`make run`, `make test`, `make lint`).
- **Testing**: Suite inicial de pruebas con `pytest` (`tests/test_api.py`).
- **Documentación**:
    - `INSTALL.md` detallado con guías de despliegue.
    - Secciones de especificaciones de hardware en `README.md`.
    - `CODE_OF_CONDUCT.md` y `AUTHORS.md`.

### Cambiado
- **Configuración**: `host/settings.py` ahora soporta configuración dinámica de `DATA_DIR` mediante variables de entorno.
- **Entrada**: `main.py` actualizado para usar `uvicorn` programáticamente.
- **Estilo**: Formateo de todo el código base con `ruff` para cumplir PEP 8.

### Corregido
- **Linting**: Arreglados imports desordenados y líneas largas en múltiples archivos.
- **Docs**: Corregidos enlaces rotos y errores tipográficos en README.

---

### 📚 Documentación Relacionada
- [README.md](README.md) | [ROADMAP.md](ROADMAP.md) | [AUTHORS.md](AUTHORS.md)
