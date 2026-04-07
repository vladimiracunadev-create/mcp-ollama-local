# Política de Seguridad y Divulgación Responsable

La seguridad, trazabilidad y observabilidad son pilares de este ecosistema de proyectos. Tomamos con la mayor seriedad cualquier reporte referente a la integridad de nuestras aplicaciones.

## Versiones Soportadas

Actualmente, solo la versión `main` (última iteración o tag de release) en los distintos repositorios recibe actualizaciones y parches de seguridad directos. Las versiones antiguas legadas bajo tags sin soporte no están cubiertas a menos que se indique estrictamente lo contrario en las notas del repositorio.

## Cómo Reportar una Vulnerabilidad

**Por favor, no reportes problemas de seguridad a través de Issues públicos de GitHub.** Esto expone la vulnerabilidad a actores maliciosos antes de que el parche pueda ser emitido.

Para reportes de seguridad, fallos críticos de integridad o configuraciones por defecto mitigables (como credenciales expuestas, RCE, inyecciones de código severas, o bypass de autenticación), sigue estos pasos:

1. **Envía un correo electrónico** directamente a `vladimir.acuna.dev@gmail.com`.
2. Incluye en tu correo:
   - El ecosistema o repositorio afectado (ej. `mcp-ollama-local`, `social-bot-scheduler`).
   - Los pasos detallados para reproducir la vulnerabilidad.
   - Opcionalmente, una prueba de concepto (PoC) en formato de script o video si aplica.
   - Posibles implicaciones de seguridad evaluadas bajo estándares técnicos.

Te contactaré a la brevedad posible (generalmente en menos de 48 horas laborales). Una vez analizado y mitigado, si deseas ser acreditado y tu hallazgo es verificable, recibirás el reconocimiento público merecido en nuestros reportes de seguridad o CHANGELOG.

¡Gracias por ayudar a mantener la infraestructura segura y profesional!

## Auditoría y Análisis Estático (SAST)

Para garantizar la integridad del código y las dependencias, el proyecto utiliza:
- **Bandit**: Analiza el código fuente en busca de patrones de programación inseguros (ej. Inyección SQL, uso de `eval`, etc.).
- **Pip-Audit**: Escanea las dependencias instaladas contra bases de datos de vulnerabilidades conocidas (CVE).
- **Ruff**: Asegura la calidad y consistencia del código, previniendo errores comunes.

Estas herramientas se ejecutan automáticamente en cada cambio a través de GitHub Actions.

## Consideraciones de Seguridad en Tools MCP

Las herramientas MCP (`list_files`, `grep_text`, `system_info`) operan dentro de un **sandbox** (`data/sandbox`). Se han implementado las siguientes protecciones:
- **Validación de Rutas**: Se impide el uso de `..` y se valida que toda ruta resuelta esté dentro del prefijo del sandbox.
- **Enmascaramiento**: `system_info` no revela rutas absolutas del sistema operativo para evitar enumeración.
- **Límites de Recursos**: Las herramientas tienen topes fijos de lectura (`max_items`, `max_hits`) para prevenir ataques de denegación de servicio (DoS) inducidos por prompts maliciosos.

## Arquitectura de Seguridad por Capas (Defense in Depth)

Hemos implementado un modelo de seguridad basado en 8 capas:

1. **Contenedor**: Proceso ejecuta como usuario no-root (`appuser`), puerto no privilegiado (8000), imágenes con versiones fijas y `HEALTHCHECK` activo.
2. **Red**: Blindaje de red en `docker-compose.yml` vinculando puertos exclusivamente a `127.0.0.1`.
3. **Credenciales**: Soporte para `API_KEY` con opción de ser obligatorio (`REQUIRE_API_KEY=true`). Archivo `.env` protegido en `.gitignore`.
4. **Servidor Web**: Cabeceras de seguridad activas (`CSP`, `HSTS`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`) y Rate Limiting básico (60 req/min).
5. **Herramientas MCP**: Aislamiento total en sandbox (`data/sandbox`) con validación de rutas y enmascaramiento de rutas del sistema host.
6. **Autenticación**: Capa de validación por cabecera `X-API-Key` en todos los endpoints sensibles.
7. **CI/CD**: Pipeline automatizado en GitHub Actions para detectar vulnerabilidades en dependencias y fallos de linting.
8. **Supply Chain**: Consistencia de line endings (`LF`) forzada vía `.gitattributes` para evitar errores de ejecución en Docker.

## Riesgos de Exposición Externa

Este repositorio está diseñado para **uso local**. Si decides exponerlo a internet o a una red compartida, ten en cuenta:
1. **Falta de Auth por Defecto**: Por defecto, cualquier persona con acceso al puerto podrá usar tu IA y sus herramientas.
2. **Uso de API_KEY**: Si vas a exponer el servicio, **debes** configurar una `API_KEY` en tu archivo `.env`.
3. **CORS**: Configura `ALLOWED_ORIGINS` para restringir qué dominios pueden interactuar con tu API.
4. **Localhost**: La configuración por defecto en `main.py` usa `127.0.0.1`. No cambies esto a `0.0.0.0` a menos que entiendas los riesgos de exposición.
