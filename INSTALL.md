# 📦 Guía de Instalación y Despliegue

Este documento detalla cómo ejecutar `mcp-ollama-local` en diferentes entornos.

## Opción 1: Local (Bare Metal)
Recomendado para desarrollo o uso personal rápido en Mac/Linux.

### Requisitos
- Python 3.13+
- `uv` (recomendado)
- Ollama corriendo localmente

### Pasos
1.  **Clonar e Instalar**:
    ```bash
    git clone https://github.com/vladimiracunadev-create/mcp-ollama-local.git
    cd mcp-ollama-local
    make install
    ```
2.  **Ejecutar**:
    ```bash
    make run
    ```
3.  **Acceder**: [http://localhost:8000](http://localhost:8000)

### Configuración Avanzada (Variables de Entorno)
Puedes personalizar el comportamiento sin tocar el código:

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `OLLAMA_URL` | URL del servidor Ollama | `http://localhost:11434` |
| `MODEL` | Modelo LLM a utilizar | `qwen2.5-coder:7b` |
| `DATA_DIR` | Ruta para base de datos y logs | `./data` (en raíz del proyecto) |

Ejemplo:
```bash
MODEL=llama3:8b make run
```

---

## Opción 2: Docker (Recomendado)
Ideal para aislar la aplicación y sus dependencias.

### Requisitos
- Docker y Docker Compose
- Ollama corriendo en el host

### Pasos
1.  **Construir y Levantar**:
    ```bash
    docker compose up --build -d
    ```
    *Nota: Esto montará `./data` localmente para persistir tu historial.*

2.  **Acceder**: [http://localhost:8000](http://localhost:8000)

3.  **Detener**:
    ```bash
    docker compose down
    ```

### ⚠️ Conexión con Ollama en Docker
La configuración por defecto asume que puedes acceder al host vía `host.docker.internal`.
- **Mac/Windows**: Funciona automáticamente.
- **Linux**: Debes asegurarte de que Docker soporte `host-gateway` (incluido en `docker-compose.yml`). Si Ollama solo escucha en `127.0.0.1`, configúralo para escuchar en `0.0.0.0` con `OLLAMA_HOST=0.0.0.0 ollama serve`.

### 📥 Descarga del Modelo (REQUERIDO)
Antes de usar la aplicación, **debes descargar un modelo LLM** en tu máquina host:
```bash
ollama pull qwen3:8b
# O cualquier otro modelo compatible
```
**Nota**: Los modelos son archivos grandes (5-20GB) que se almacenan localmente. NO se incluyen en el repositorio de GitHub.

---

## Opción 3: Kubernetes (K8s)
Para despliegues escalables o en clústeres domésticos.

### Pasos
1.  **Construir Imagen** (o usar registro):
    ```bash
    docker build -t mcp-ollama-local:latest .
    # Si usas minikube/kind, carga la imagen en el nodo primero.
    ```

2.  **Aplicar Manifiestos**:
    ```bash
    kubectl apply -f k8s/deploy.yaml
    kubectl apply -f k8s/service.yaml
    ```

3.  **Acceder**:
    Haz un Port-Forward al servicio:
    ```bash
    kubectl port-forward svc/mcp-ollama-service 8080:80
    ```
    Visita [http://localhost:8080](http://localhost:8080).

### Nota sobre Persistencia en K8s
El despliegue usa un `PersistentVolumeClaim` (PVC) de 1GB. Asegúrate de tener configurado un StorageClass por defecto en tu clúster.
