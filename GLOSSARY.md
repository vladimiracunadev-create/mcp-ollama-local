# Glosario Técnico del Proyecto

Si el flujo técnico de este ecosistema te resulta ajeno en algunos aspectos, aquí tienes un diccionario práctico:

| Término | Significado en este Proyecto |
| --- | --- |
| **Model Context Protocol (MCP)** | Una iniciativa Open-Source (liderada por Anthropic) orientada a dar a los grandes modelos de lenguaje una interfaz universal (una "API unificada") a orígenes de datos y herramientas sin exponer integraciones Custom o RAGs mal hechos mediante hard-coding. |
| **Ollama** | La "Placa base" de la IA en este proyecto que te permite descargar LLMs grandes y ejecutarlos en la CPU/GPU de tu propia máquina. API-local 100%. |
| **FastAPI** | Framework en Python elegido por su excepcional asincronicidad. Lo usamos como fachada o UI (Server-side rendering), y no como un micro-servicio puro. |
| **Sandbox / File-System Enjaulado** | Principio de ciber-seguridad: El Agente IA no tiene permiso para consultar toda tu unidad de disco (C:// ó /MacHD), sino restringido a `data/sandbox`. |
| **Rootless Container** | Práctica Docker para no usar al super-usuario de Linux (root) en tiempo de ejecución de la App para mitigar escapes y elevaciones de privilegios si el contenedor es hackeado. |
| **Liveness / Readiness Probe** | Endpoint nativo `/api/health` para que el orquestador (*Kubernetes*) confirme de forma sistemática que la IA está despierta (*Liveness*) o si ha terminado de cargar antes de enviarle clientes (*Readiness*). |
| **Pydantic** | Nuestro validador de configuración estricto pre-carga, para rechazar inputs o `.env` malformados. |
| **uv** | Nuestro gestor de paquetes alterno a Pip/Poetry/Pipenv. Está escrito velozmente y garantiza reproducciones exactas de dependencias usando su manifiesto `uv.lock`. |
