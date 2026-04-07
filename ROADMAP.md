# 🗺️ Hoja de Ruta (Roadmap)

## Vision General del Proyecto

```mermaid
timeline
    title Evolucion de mcp-ollama-local
    section Completado
        v1.0.0 : Plataforma base FastAPI + Ollama
               : Protocolo MCP integrado
               : Herramientas list_files grep_text system_info
               : Persistencia SQLite
        v1.0.x : Autenticacion API_KEY
               : Hardening seguridad 8 capas
               : Docker y Kubernetes listos
               : Pipeline CI/CD GitHub Actions
    section En Progreso
        v1.1.0 : Soporte multi-modelo simultaneo
               : Interfaz con tema oscuro
    section Futuro
        v1.2.0 : Ejecucion de comandos seguros
               : Logging avanzado y monitoreo
               : Exportar e importar historial
        v2.0.0 : Integracion llama.cpp
               : App movil complementaria
               : Analisis de conversaciones
```

## 🚀 Versiones Futuras

### v1.1.0 (Proxima)
- [ ] Agregar soporte para múltiples modelos en Ollama simultáneamente.
- [ ] Mejorar la interfaz de usuario con temas oscuros.
- [x] Implementar autenticación básica (`API_KEY`).
- [x] Hardening de seguridad integral (8 capas).

### v1.2.0
- [ ] Soporte para ejecución de comandos seguros.
- [ ] Integrar logging avanzado y monitoreo de uso.
- [ ] Soporte para exportar/importar historial de chat.

## 🔮 Ideas a Largo Plazo
- Integración con otros proveedores de IA locales (ej. llama.cpp).
- Aplicación móvil complementaria.
- Análisis de conversaciones para insights.

---

### 📚 Documentación Relacionada
- [README.md](README.md) | [CHANGELOG.md](CHANGELOG.md) | [RECRUITER.md](RECRUITER.md)