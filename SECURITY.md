# 🛡️ Security Policy

## 🎯 Scope

Este repositorio es una aplicación local-first para uso individual o de laboratorio. La postura de seguridad está orientada a:

- reducir exposición accidental,
- acotar el alcance de las tools MCP,
- endurecer defaults,
- y hacer verificables los checks básicos en local y CI.

No está diseñado como servicio multiusuario expuesto a internet sin un reverse proxy, autenticación más fuerte y controles operacionales adicionales.

## 🏗️ Supported versions

Solo la rama `main` recibe correcciones activas.

## 🔓 Reportar vulnerabilidades

No publiques vulnerabilidades explotables en issues públicos.

Envía un reporte a `vladimir.acuna.dev@gmail.com` con:

- repositorio afectado,
- impacto,
- pasos de reproducción,
- versión o commit,
- y, si aplica, PoC mínima.

## 🔐 Controles implementados

### Aplicación

- Validación de payload en endpoints JSON.
- Manejo explícito de errores para requests inválidas y fallos de upstream.
- API key opcional mediante `X-API-Key`; cuando `REQUIRE_API_KEY=true`, es obligatoria.
- Rate limiting simple en memoria.
- Cabeceras web: `CSP`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.
- `Strict-Transport-Security` solo se emite bajo HTTPS real.

### Integración con Ollama

- Timeouts explícitos.
- Mensajes de error más trazables cuando Ollama no responde o devuelve payload inválido.
- No se exponen secretos del servidor al cliente por defecto.

### MCP / filesystem

- Las tools MCP operan solo dentro de `data/sandbox`.
- Se bloquean rutas con `..` y escapes fuera del sandbox.
- No hay ejecución arbitraria de comandos del sistema.

### Persistencia

- SQLite local para historial.
- El archivo vive bajo `DATA_DIR`; no hay cifrado en reposo incorporado.

### Contenedor

- Imagen multi-stage.
- Usuario no-root.
- Puerto de aplicación no privilegiado.
- `docker-compose.yml` publica solo en `127.0.0.1`.

## ✅ Validación reproducible

Local:

```bash
make lint
make test
make audit
make ci-local
```

CI:

- `.github/workflows/ci.yml`: contrato principal de calidad
- `.github/workflows/security.yml`: `bandit` + `pip-audit`

Notas:

- `make audit` es offline-friendly: usa `bandit` + `pip check`.
- `pip-audit` requiere acceso a advisories externos y por eso vive en el workflow de seguridad.

## 🔎 Verificación externa complementaria

El proyecto puede revisarse también con herramientas externas de análisis, incluyendo SafeSkill, siempre como capa complementaria y no como criterio principal de confianza.

Ejemplos:

```bash
npx skillsafe scan .
npx skillsafe scan . --json > safeskill-report.json
```

En términos generales, este tipo de herramienta puede ayudar a detectar o resaltar:

- comportamiento de red y dependencias externas observables,
- acceso a archivos y superficie de interacción con el host,
- patrones asociados a prompt injection o uso riesgoso de tools,
- discrepancias entre lo que el repositorio declara y lo que realmente implementa.

Interpretación recomendada:

- trata los resultados como insumo para revisión, no como veredicto final,
- valida cada finding contra el código, la configuración y el contexto operativo,
- distingue entre exposición real, decisión consciente de diseño y falso positivo,
- y no conviertas un score externo en una “nota oficial” del proyecto.

Si se comparte un reporte externo en un issue o PR, debe acompañarse de explicación técnica, impacto y propuesta concreta de corrección cuando corresponda.

## 🚧 Límites y no-objetivos

- No hay autenticación de usuarios ni sesiones.
- No hay protección contra un operador local malicioso.
- No hay aislamiento de proceso tipo VM o container por cada tool call.
- El rate limiting no sustituye WAF, API gateway ni controles distribuidos.
- CORS no es un control de autenticación.
- Si expones la app fuera de localhost, debes añadir TLS, reverse proxy, autenticación más fuerte y observabilidad operativa.

## ⚠️ Falsos positivos frecuentes

Hallazgos que suelen aparecer en escáneres genéricos y requieren contexto:

- `B104` por bind en `0.0.0.0` dentro de contenedor: aceptable cuando el publish externo sigue restringido a `127.0.0.1` en compose.
- “No HSTS”: correcto cuando el entorno de desarrollo sirve HTTP plano; HSTS solo tiene sentido detrás de HTTPS.
- “Wildcard CORS”: sería hallazgo real si se configurara `*`; el default actual es una lista local explícita.
- “SQLite insecure”: depende del contexto. Aquí el riesgo principal no es SQL injection sino exposición del host o permisos de filesystem.

## 🤝 Política de contribuciones de seguridad

Se priorizan PRs que:

- corrijan una debilidad demostrable,
- incluyan validación o test,
- documenten límites y trade-offs,
- y mantengan compatibilidad operativa.

Un badge externo o un enlace a un escáner no reemplaza fixes técnicos verificables.
