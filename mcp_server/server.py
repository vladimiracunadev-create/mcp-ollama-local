from __future__ import annotations

import platform
import shutil
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-local-tools")

BASE = Path(__file__).resolve().parents[1]
SANDBOX = (BASE / "data" / "sandbox").resolve()

def safe_sandbox_path(rel: str) -> Path:
    p = (SANDBOX / rel).resolve()
    if not str(p).startswith(str(SANDBOX)):
        raise ValueError("Ruta fuera de sandbox (bloqueado).")
    return p

@mcp.tool()
def list_files(rel_dir: str = ".", max_items: int = 200) -> dict:
    """Lista archivos/carpetas dentro de data/sandbox (modo seguro)."""
    d = safe_sandbox_path(rel_dir)
    if not d.exists() or not d.is_dir():
        return {"ok": False, "error": f"No existe o no es directorio: {d}"}

    items = []
    for i, entry in enumerate(sorted(d.iterdir(), key=lambda x: x.name.lower())):
        if i >= max_items:
            break
        items.append({
            "name": entry.name,
            "type": "dir" if entry.is_dir() else "file",
            "size": entry.stat().st_size if entry.is_file() else None,
        })
    return {"ok": True, "dir": str(d), "items": items}

@mcp.tool()
def grep_text(needle: str, rel_dir: str = ".", max_hits: int = 50) -> dict:
    """Busca needle en archivos de texto/código dentro de data/sandbox."""
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
            except Exception:
                continue
            if needle.lower() in text.lower():
                hits.append(str(f.relative_to(SANDBOX)))
    return {"ok": True, "needle": needle, "hits": hits}

@mcp.tool()
def system_info() -> dict:
    """Info útil del sistema y disco (en el proyecto)."""
    total, used, free = shutil.disk_usage(str(BASE))
    return {
        "os": platform.platform(),
        "python": platform.python_version(),
        "project_root": str(BASE),
        "sandbox": str(SANDBOX),
        "disk_total_gb": round(total / (1024**3), 2),
        "disk_free_gb": round(free / (1024**3), 2),
    }

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
