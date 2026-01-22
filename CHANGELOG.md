# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [0.1.0] - 2026-01-22

### Añadido
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
