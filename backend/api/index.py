import importlib
import sys
import traceback
from pathlib import Path

# Add backend directory to sys.path so app modules import cleanly on Vercel
current_dir = Path(__file__).resolve().parent
candidates = [
    str(current_dir / "backend"),
    str(current_dir.parent / "backend"),
    str(current_dir.parent),
    str(current_dir),
]
for p in candidates:
    if Path(p).is_dir() and (Path(p) / "app").is_dir() and p not in sys.path:
        sys.path.insert(0, p)

_app_instance = None
try:
    try:
        from app.main import app as _real_app
    except ImportError:
        _mod = importlib.import_module("backend.app.main")
        _real_app = getattr(_mod, "app")
    _app_instance = _real_app
except Exception as _e:
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    _err = traceback.format_exc()
    print("FATAL VERCEL PYTHON STARTUP ERROR:\n" + _err, file=sys.stderr, flush=True)

    _err_app = FastAPI(title="PowerManage Diagnostics")

    @_err_app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    async def _handle_startup_error(full_path: str = ""):
        return PlainTextResponse(f"FastAPI Startup Error:\n\n{_err}", status_code=500)

    _app_instance = _err_app

# Unindented, column-0 assignment required by Vercel static AST parser
app = _app_instance
