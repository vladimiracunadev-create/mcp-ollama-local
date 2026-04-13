# Reglas Semgrep del repositorio

Estas reglas no intentan sustituir CodeQL, Bandit ni revisión humana.

Su objetivo es capturar drift específico del contexto de `mcp-ollama-local`, donde importan especialmente:

- timeouts explícitos en llamadas HTTP,
- ausencia de `shell=True`,
- coherencia con el modelo local-first,
- evitar CORS wildcard,
- y no introducir defaults secretos en código.
