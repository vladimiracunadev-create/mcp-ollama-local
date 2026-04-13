# 🔎 Verificación de seguridad complementaria

Este repositorio mantiene una separación explícita entre:

- validación propia y reproducible del proyecto,
- y señales externas de verificación complementaria.

La base de confianza sigue estando en los controles internos del repositorio:

- `make lint`
- `make format-check`
- `make test`
- `make audit`
- `make ci-local`

Para la vista completa del sistema de controles, señales públicas y evidencia de supply chain, consulta [docs/security-trust-profile.md](security-trust-profile.md).

## 🧪 Uso opcional de SafeSkill

SafeSkill puede ejecutarse desde terminal sin convertirlo en dependencia estructural del proyecto:

```bash
npx skillsafe scan .
npx skillsafe scan . --json > safeskill-report.json
```

Esto permite obtener una lectura externa adicional sobre el estado del repositorio, especialmente útil durante revisiones manuales, mantenimiento o discusión de hallazgos en PRs.

## 📡 Qué tipo de señales puede aportar

En términos generales, SafeSkill puede ayudar a resaltar:

- comportamiento de red,
- acceso a archivos y relación con el host,
- patrones de prompt injection,
- correlación entre contenido documental y comportamiento del código.

Estas señales son útiles, pero no deben leerse de forma aislada.

## 🧠 Cómo interpretar resultados

- Un hallazgo no equivale automáticamente a vulnerabilidad explotable.
- Un resultado “sin findings” no demuestra ausencia de riesgo.
- Un score externo no sustituye revisión de código, pruebas ni conocimiento del contexto de despliegue.
- Los findings deben contrastarse con arquitectura, configuración, defaults y límites documentados.

## 📌 Postura del proyecto

El repositorio acepta escrutinio externo y lo considera valioso cuando:

- aporta contexto verificable,
- ayuda a priorizar riesgos reales,
- y deriva en fixes técnicos concretos.

No se usa un badge externo como señal principal de calidad del producto ni como evidencia suficiente de madurez de seguridad.
