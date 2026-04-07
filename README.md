# 🧠 MCP Ollama Local

[![SafeSkill 89/100](https://img.shields.io/badge/SafeSkill-89%2F100_Passes%20with%20Notes-yellow)](https://safeskill.dev/scan/vladimiracunadev-create-mcp-ollama-local)

> **Web Local (FastAPI) + IA Local (Ollama) + Herramientas MCP**

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Hardening](https://img.shields.io/badge/security-8--layers-blueviolet.svg)

---

**mcp-ollama-local** es una plataforma ligera diseñada para ejecutar un entorno de chat con IA completamente local, integrando la potencia de **Ollama** con la flexibilidad del **Model Context Protocol (MCP)**.  

Permite conversar con LLMs locales (como `qwen`, `llama3`, etc.) y otorgarles capacidades reales mediante herramientas seguras (acceso a archivos, búsqueda, información del sistema), todo con persistencia en SQLite.

> [!TIP]
> 🎓 **¿Nuevo en IA o Docker?** Consulta nuestro [Manual para Principiantes (USER_MANUAL.md)](USER_MANUAL.md) para entender conceptos básicos y por qué esto es útil para ti.

---

## 🚀 Características Principales

- **🗣️ Chat Conversacional**: Interfaz web limpia para interactuar con tus modelos locales.
- **🔌 Protocolo MCP**: Integración nativa para expandir las capacidades del modelo.
- **🛠️ Herramientas Seguras**: Incluye herramientas de sistema (`system_info`, `list_files`, `grep_text`).
- **💾 Historial Persistente**: Guardado de conversaciones en SQLite.
- **🛡️ Seguridad en 8 Capas**: Protección integral desde el contenedor hasta la red.
- **🔒 Privacidad Total**: Todo corre en tu máquina (`localhost`), 100% privado.
- **🐳 Cloud Native**: Listo para Docker y Kubernetes (K8s).

## 🏗️ Arquitectura

Todo corre **100% local** en tu máquina. Cuatro capas bien definidas:

```mermaid
graph LR
    subgraph CLIENTE["  Cliente  "]
        U["Navegador Web"]
    end

    subgraph BACKEND["  Backend - Docker  "]
        API["FastAPI Backend"]
        DB["SQLite Historial"]
    end

    subgraph IA["  Motor de IA  "]
        OL["Ollama LLM Local"]
    end

    subgraph TOOLS["  Herramientas MCP  "]
        MCP["MCP Server"]
        SB["Sandbox - Zona Segura"]
    end

    U -->|HTTP| API
    API -->|Guarda sesion| DB
    API -->|Prompt + Historial| OL
    OL -->|Tool Call| MCP
    MCP -->|Acceso controlado| SB
    MCP -->|Resultado| OL
    OL -->|Respuesta final| API
    API -->|HTML| U

    style CLIENTE fill:#1e3a5f,color:#e2e8f0,stroke:#60a5fa
    style BACKEND fill:#14532d,color:#e2e8f0,stroke:#4ade80
    style IA fill:#4a1d96,color:#e2e8f0,stroke:#a78bfa
    style TOOLS fill:#78350f,color:#e2e8f0,stroke:#fbbf24
```

## 📊 Requisitos del Sistema

Para garantizar un rendimiento fluido, se recomiendan las siguientes especificaciones:

*   **CPU**: Apple Silicon (M1/M2/M3) o CPU con soporte AVX2.
*   **RAM**: 8 GB (mínimo) / 16 GB (recomendado).
*   **Ollama**: Instalado y ejecutándose (`ollama serve`).
*   **Modelo**: Al menos un modelo descargado (ej. `ollama pull qwen2.5-coder:7b`).

## 📥 Modos de Despliegue

| Entorno | Comando Rápido |
| :--- | :--- |
| **💻 Local** | `make install && make run` |
| **🐳 Docker** | `docker compose up -d` |
| **☸️ Kubernetes** | `kubectl apply -f k8s/` |

> [!NOTE]
> Para instrucciones detalladas, consulta la [Guía de Instalación (INSTALL.md)](INSTALL.md).

## 🧮 Comandos del Makefile

| Comando | Descripción |
| :--- | :--- |
| `make install` | Configura entorno y dependencias. |
| `make run` | Inicia el servidor en puerto 8000. |
| `make lint` | Ejecuta auditoría de código con **Ruff/Bandit**. |
| `make test` | Ejecuta la suite de pruebas con **Pytest**. |

## 🛡️ Seguridad (Defensa en Profundidad)

Este proyecto implementa un modelo de seguridad robusto de **8 capas**:

1.  **📦 Contenedor**: Ejecución no-root (`appuser`) y puerto no privilegiado.
2.  **🌐 Red**: Bind restringido a `127.0.0.1` en Docker Compose.
3.  **🔑 Credenciales**: Soporte nativo para `API_KEY`.
4.  **🕸️ Servidor Web**: Cabeceras `CSP`, `HSTS` y Rate Limiting.
5.  **🛠️ Tools MCP**: Sandbox estricto para acceso a archivos.
6.  **🔍 Autenticación**: Validación `X-API-Key` obligatoria (opcional).
7.  **🚀 CI/CD**: Escaneo de vulnerabilidades (`Bandit`/`Pip-Audit`).
8.  **⚙️ Supply Chain**: Control de integridad vía `.gitattributes`.

## 🤝 Comunidad y Contribución

- **📜 Changelog**: Consulta el [CHANGELOG.md](CHANGELOG.md).
- **✨ Créditos**: Conoce a los autores en [AUTHORS.md](AUTHORS.md).
- **💡 Contribución**: Lee [CONTRIBUTING.md](CONTRIBUTING.md).
- **⚖️ Código de Conducta**: Consulta [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 📚 Documentación Completa

- [📖 Instalación (INSTALL.md)](INSTALL.md)
- [🎓 Manual (USER_MANUAL.md)](USER_MANUAL.md)
- [🕴️ RECRUITER (RECRUITER.md)](RECRUITER.md)
- [🗺️ Arquitectura (FILE_ARCHITECTURE.md)](FILE_ARCHITECTURE.md)
- [🛡️ Seguridad (SECURITY.md)](SECURITY.md)
- [🔧 Troubleshooting (TROUBLESHOOTING.md)](TROUBLESHOOTING.md)
- [🗺️ Roadmap (ROADMAP.md)](ROADMAP.md)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.
