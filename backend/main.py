import sys
from pathlib import Path

# Ensure backend root is in sys.path for Vercel
backend_root = str(Path(__file__).resolve().parent)
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from app.main import app  # noqa: F401
