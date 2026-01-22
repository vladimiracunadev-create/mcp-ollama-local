# Guía para Contribuir

¡Gracias por tu interés en hacer `mcp-ollama-local` mejor!

## Inicio Rápido

El proyecto usa `Makefile` para simplificar el desarrollo.

1.  **Forkea y Clona** el repositorio.
2.  **Instala dependencias**:
    ```bash
    make install
    ```
3.  **Crea una rama**: `git checkout -b feature/mi-mejora`

## Flujo de Trabajo

Antes de enviar tu Pull Request, asegúrate de cumplir con los estándares de calidad:

- **Linting**: El código debe estar limpio.
    ```bash
    make lint
    # Si hay errores, puedes intentar corregirlos automáticamente con:
    make format
    ```
- **Tests**: Asegúrate de no romper nada existente.
    ```bash
    make test
    ```

## Estilo de Código y Commits

- **Python**: Usamos `ruff` para mantener el estilo PEP 8 automáticamente.
- **Commits**: Recomendamos usar [Conventional Commits](https://www.conventionalcommits.org/).
    - `feat: nueva funcionalidad`
    - `fix: corrección de bug`
    - `docs: mejoras en documentación`
    - `style: formateo, espacios en blanco`

## Reportar Problemas

Si encuentras un bug, por favor abre un Issue incluyendo:
- Pasos para reproducir.
- Comportamiento esperado vs real.
- Tu entorno (SO, versión de Python/Ollama).

¡Esperamos tus PRs!