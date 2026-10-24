import sys
from pathlib import Path

# Ensure backend root is in sys.path for Vercel function imports
backend_root = str(Path(__file__).resolve().parent.parent)
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from app.main import app

# Top-level application assignment for Vercel Python entrypoint
app = app
