# Contributing

Gracias por contribuir.

El criterio de aceptación del proyecto prioriza consistencia, fixes verificables y deuda técnica visible por encima de marketing o claims inflados.

## Flujo esperado

1. Parte desde `main`.
2. Mantén el cambio acotado y justificable.
3. Añade o ajusta tests si cambias comportamiento.
4. Actualiza documentación si cambias comandos, defaults o límites.
5. Ejecuta antes de abrir PR:

```bash
make lint
make format-check
make test
make audit
```

Opcionalmente, si quieres aportar contexto adicional en un PR de seguridad o hardening, puedes adjuntar una verificación externa complementaria:

```bash
npx skillsafe scan .
npx skillsafe scan . --json > safeskill-report.json
```

No es un requisito de contribución. Si lo usas, resume los hallazgos relevantes con criterio técnico en lugar de adjuntar solo un score o badge.

## Qué tipo de cambios sí ayudan

- fixes de bugs con reproducción clara,
- endurecimiento de seguridad con evidencia,
- mejoras de validación local o CI,
- documentación alineada con la implementación,
- mejoras de UX técnica sin sobrecargar la UI.

## Qué tipo de cambios normalmente no se aceptan solos

- badges externos en README,
- promesas de seguridad sin controles verificables,
- placeholders o texto aspiracional,
- refactors grandes sin beneficio operativo claro,
- dependencia nueva pesada sin justificación fuerte.

## Estilo y alcance

- Usa Python 3.13 y el flujo con `uv`.
- No introduzcas Node/npm salvo necesidad técnica real.
- Mantén la UI simple; este repo no necesita una build chain frontend.
- Si cambias configuración, refleja el cambio en `README.md`, `INSTALL.md` o `SECURITY.md`.

## Pull requests de seguridad o escaneo

Si propones una mejora de seguridad:

- incluye el hallazgo real,
- explica impacto y condiciones de explotación,
- aporta fix verificable,
- y añade validación o test cuando corresponda.

Un PR que solo agregue un badge o enlace a un escáner externo no se considera una mejora suficiente del producto.
