import uvicorn


def main():
    """Ejecuta el servidor de desarrollo local."""
    print("Iniciando servidor mcp-ollama-local...")
    uvicorn.run("apps.web.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
