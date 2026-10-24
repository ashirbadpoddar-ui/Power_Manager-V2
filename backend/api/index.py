import sys
import traceback
from pathlib import Path

# Add backend root and parent directories to sys.path so app modules import cleanly on Vercel
backend_root = Path(__file__).resolve().parent.parent
for p in [str(backend_root), str(backend_root.parent)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app.main import app
except Exception as e:
    err_tb = traceback.format_exc()
    print("CRITICAL VERCEL FASTAPI STARTUP ERROR:\n" + err_tb, file=sys.stderr, flush=True)

    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse

    app = FastAPI(title="PowerManage Startup Diagnostic")

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    async def startup_error_fallback(full_path: str = ""):
        return PlainTextResponse(
            f"Vercel Serverless Function Startup Error:\n\n{err_tb}\n"
            f"Please verify your Vercel Environment Variables (e.g. DATABASE_URL).",
            status_code=500,
        )
