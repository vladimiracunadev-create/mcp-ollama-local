# ¿Cómo Activar Modelos Locales IA (Ollama) en esta Arquitectura?

La gracia de **mcp-ollama-local** es que desacopla la descarga y ejecución pura del modelo (gestionado nativamente por Ollama) del consumo orquestado usando la estandarización Model Context Protocol (gestionado aquí en FastAPI).

Esta es la guía estandarizada para activar un modelo, desde la descarga hasta tenerlo funcional consumiendo herramientas locales (MCP).

## Paso 1: Instalar el Daemon de Ollama Local
Ollama actúa como nuestro motor.
- **Mac:** Descarga la app nativa desde [Ollama.com/download](https://ollama.com/download). 
- **Linux:** Ejecuta `curl -fsSL https://ollama.com/install.sh | sh`
- **Windows:** Bájalo usando el WSL2 soportado.

Inicia el servicio en segundo plano (Normalmente `ollama serve` o abriendo la app en Mac). Comprueba que funciona navegando a:
👉 `http://localhost:11434` (Debe responder _"Ollama is running"_).

## Paso 2: Importar / Descargar Modelos

Por defecto este proyecto asume que un LLM capaz de procesar **Calling Functions** eficientemente corre bajo el capó. Usa la CLI para bajar el modelo que necesites, tu máquina requerirá conexión a internet por esta única y última vez.

Recomendamos **Qwen 2.5 Coder 7B**, es un genio absoluto para *Tools*:
```bash
ollama pull qwen2.5-coder:7b
```

Otras alternativas soportadas (si tienes RAM suficiente, +16GB):
```bash
ollama pull llama3
ollama pull mistral-nemo
```

## Paso 3: Configurar Tu Entorno Local (`.env`)

Con el modelo ya almacenado en el caché de Ollama en tu sistema, diremos a nuestra App qué modelo cargar predeterminadamente.

Por defecto, en `host/settings.py`, la aplicación llama a `qwen2.5-coder:7b` en `http://localhost:11434`. Si usaste un modelo diferente (como `llama3`), créate un archivo `.env` en la raíz de `mcp-ollama-local`:

```env
MODEL=llama3
OLLAMA_URL=http://localhost:11434
# DATA_DIR=./data  # Puedes cambiar la ruta de la SQLite también
```

## Paso 4: Activar el Ecosistema

Usa el entorno hiper-optimizado que construimos en el puerto 8000:
```bash
make run
```

Al navegar a `http://localhost:8000/`, verás el chat que internamente ya ha enlazado el sub-proceso MCP al modelo que hayas seleccionado en tu `.env`. ¡A disfrutar la IA Local y privada!
