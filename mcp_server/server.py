from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-local-tools")

BASE = Path(__file__).resolve().parents[1]
SANDBOX = (BASE / "data" / "sandbox").resolve()


def safe_sandbox_path(rel: str) -> Path:
    # Evitar que suba niveles con .. antes de resolver
    if ".." in rel:
        raise ValueError("Ruta con '..' detectada (bloqueado).")
    
    p = (SANDBOX / rel).resolve()
    
    # Verificación robusta: el sandbox debe ser el prefijo común
    if os.path.commonpath([str(p), str(SANDBOX)]) != str(SANDBOX):
        raise ValueError("Ruta fuera de sandbox (bloqueado).")
    return p


@mcp.tool()
def list_files(rel_dir: str = ".", max_items: int = 200) -> dict:
    """Lista archivos/carpetas dentro de data/sandbox (modo seguro)."""
    # Hard cap para evitar abuso por prompt injection
    max_items = min(max_items, 1000)
    d = safe_sandbox_path(rel_dir)
    if not d.exists() or not d.is_dir():
        return {"ok": False, "error": f"No existe o no es directorio: {d}"}

    items = []
    for i, entry in enumerate(sorted(d.iterdir(), key=lambda x: x.name.lower())):
        if i >= max_items:
            break
        items.append(
            {
                "name": entry.name,
                "type": "dir" if entry.is_dir() else "file",
                "size": entry.stat().st_size if entry.is_file() else None,
            }
        )
    return {"ok": True, "dir": str(d), "items": items}


@mcp.tool()
def grep_text(needle: str, rel_dir: str = ".", max_hits: int = 50) -> dict:
    """Busca needle en archivos de texto/código dentro de data/sandbox."""
    # Hard cap para evitar abuso de recursos
    max_hits = min(max_hits, 100)
    d = safe_sandbox_path(rel_dir)
    if not d.exists() or not d.is_dir():
        return {"ok": False, "error": f"No existe o no es directorio: {d}"}

    exts = {".txt", ".md", ".py", ".js", ".json", ".html", ".css"}
    hits = []
    for f in d.rglob("*"):
        if len(hits) >= max_hits:
            break
        if f.is_file() and f.suffix.lower() in exts:
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:  # nosec B112 - Ignorar archivos ilegibles intencionalmente
                continue
            if needle.lower() in text.lower():
                hits.append(str(f.relative_to(SANDBOX)))
    return {"ok": True, "needle": needle, "hits": hits}


@mcp.tool()
def system_info() -> dict:
    """Info básica del sistema (restringida)."""
    total, used, free = shutil.disk_usage(str(BASE))
    return {
        "os": platform.system(),
        "python": platform.python_version(),
        "disk_total_gb": round(total / (1024**3), 2),
        "disk_free_gb": round(free / (1024**3), 2),
        "status": "Healthy (restricted mode)",
    }


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
