# 🔧 Troubleshooting

> [!NOTE]
> Empieza por `/api/health`. En este proyecto suele decir más sobre el estado real del sistema que la UI por sí sola.

## 1. `/api/health` marca `ollama_ok=false`

Verifica:

```bash
curl -sS http://localhost:11434/api/tags
```

Si no responde:

- inicia Ollama,
- revisa `OLLAMA_URL`,
- confirma que el modelo existe con `ollama list`.

## 2. Docker no alcanza Ollama

Síntoma típico:

```text
Could not connect to Ollama at http://host.docker.internal:11434
```

Pasos:

```bash
docker compose ps
docker compose logs --tail=50 app
```

En Linux, revisa que:

- `host.docker.internal` resuelva,
- Docker soporte `host-gateway`,
- y Ollama no esté atado solo a `127.0.0.1`.

## 3. La API responde 403

Revisa si activaste:

```bash
REQUIRE_API_KEY=true
API_KEY=...
```

En ese caso debes enviar:

```bash
curl -sS http://127.0.0.1:8000/api/health -H 'X-API-Key: tu-clave'
```

## 4. `make audit` falla

Qué valida hoy:

- `bandit`
- `python -m pip check`

Si falla `pip-audit` en CI o en un entorno con red restringida, el problema puede ser conectividad hacia la base de advisories y no una vulnerabilidad del código.

## 5. No aparece historial

El historial se crea en `DATA_DIR/chat_history.sqlite` cuando el chat guarda mensajes.

Comprueba:

```bash
ls -la data
curl -sS http://127.0.0.1:8000/api/history
```

## 6. El frontend queda “procesando”

Pasos rápidos:

- abre DevTools y revisa la request a `/api/chat` o `/api/mcp`,
- consulta `/api/health`,
- verifica logs del servidor,
- prueba el endpoint con `curl` para aislar si el problema es UI o backend.
