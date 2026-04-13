# 🛡️ Security & Trust Profile

Este documento describe el perfil de seguridad y confianza del repositorio como un sistema de controles complementarios, no como una sola herramienta o una sola nota pública.

## 🎯 Objetivo del perfil

El proyecto prioriza, en este orden:

1. seguridad reproducible
2. coherencia entre documentación y código
3. controles visibles en CI
4. reglas propias adaptadas al contexto del repo
5. señales públicas complementarias
6. trazabilidad de supply chain

## 🧱 Qué controles se ejecutan

### Local

- `make lint`: calidad estática con Ruff
- `make test`: regresión funcional básica
- `make audit`: Bandit + compatibilidad de dependencias instaladas
- `make semgrep`: reglas Semgrep propias del repositorio
- `make sbom`: genera SBOM CycloneDX desde la `.venv`
- `make ci-local`: contrato base de calidad
- `make trust-check`: `ci-local` + Semgrep + SBOM

### CI

- `ci.yml`: contrato principal de calidad reproducible
- `security.yml`: Bandit + `pip-audit`
- `codeql.yml`: code scanning semántico para Python
- `semgrep.yml`: reglas locales y upload SARIF
- `scorecard.yml`: señal pública complementaria de higiene del repositorio
- `supply-chain.yml`: SBOM y firma de artefactos de release

## 🔍 Qué cubre cada herramienta

### Ruff

Cubre estilo, imports, errores obvios y consistencia básica.

No cubre:

- vulnerabilidades semánticas complejas,
- supply chain,
- ni decisiones inseguras de arquitectura.

### Pytest

Cubre regresiones funcionales de rutas críticas del backend.

No cubre:

- toda la superficie de integración con Ollama real,
- ni pruebas end-to-end de Docker/Kubernetes.

### Bandit

Cubre patrones inseguros frecuentes en Python.

No cubre:

- drift entre documentación y comportamiento,
- vulnerabilidades de dependencias,
- ni decisiones locales específicas del repo.

### pip-audit

Cubre vulnerabilidades conocidas en dependencias Python resueltas por bases de advisories.

No cubre:

- paquetes sin advisory público,
- fallos lógicos en el código del proyecto,
- ni contexto de explotación real.

### CodeQL

Cubre code scanning semántico más profundo que un linter tradicional.

No cubre:

- todas las decisiones operativas del despliegue,
- ni la validez de claims documentales.

### Semgrep con reglas propias

Cubre drift específico del repositorio:

- timeouts HTTP ausentes,
- `shell=True`,
- CORS wildcard,
- bind Python abierto en `0.0.0.0`,
- defaults hardcoded para `API_KEY`.

No cubre:

- todos los flujos de datos complejos,
- ni reemplaza revisión manual.

### CycloneDX SBOM

Cubre inventario reproducible de componentes del entorno Python usado por el proyecto.

No cubre:

- ausencia de vulnerabilidades,
- ni integridad criptográfica por sí solo.

### Cosign

Cubre firma y verificación de blobs generados en release, como el SBOM.

No cubre:

- seguridad del código fuente por sí misma,
- ni reemplaza control de cambios y revisión.

### OpenSSF Scorecard

Cubre una señal pública agregada sobre prácticas del repositorio.

No cubre:

- calidad del producto,
- seguridad del runtime,
- ni contexto específico del proyecto.

## 🧠 Qué hallazgos requieren juicio humano

- findings de CodeQL o Semgrep que dependen del modo de despliegue
- hallazgos sobre exposición de red en contenedor versus local
- findings de dependencias que no son explotables en este contexto
- divergencias entre score público y controles reales del repo
- reportes externos que no incluyen reproducción ni fix verificable

## 🧩 Reglas propias del repositorio

Las reglas Semgrep viven en [`semgrep-rules/`](/Volumes/ORICO/LabMCP/mcp-ollama-local/semgrep-rules/README.md) y están pensadas para proteger supuestos concretos del proyecto:

- local-first por defecto
- integración HTTP con timeout explícito
- ausencia de ejecución shell abierta
- CORS no wildcard
- secretos no hardcodeados

## 🌐 Qué señales públicas verán terceros

- Code scanning en GitHub con CodeQL y SARIF adicional
- Dependabot para dependencias y workflows
- Scorecard como señal secundaria
- SBOM como evidencia de inventario de componentes
- firma Cosign en artefactos de release cuando aplique

El repositorio no depende de una sola puntuación ni de un badge externo para sostener su valor técnico.

## 🔗 Cadena de suministro y trazabilidad

- `uv.lock` fija el grafo Python del proyecto
- `make sbom` genera un inventario CycloneDX de la `.venv`
- `supply-chain.yml` adjunta el SBOM como artefacto
- en releases, el SBOM se firma con Cosign keyless usando OIDC de GitHub Actions

## 📣 Qué mensaje transmite esto a terceros

El repositorio acepta escrutinio, expone controles verificables y evita convertir una herramienta externa en autoridad única. Eso transmite criterio técnico, mantenimiento activo y una postura de seguridad que puede sostenerse con evidencia.
