"""
Vercel Entrypoint

Este arquivo é o entrypoint para deploy no Vercel.
Simplesmente exporta a aplicação FastAPI.
"""

import sys
import traceback

try:
    from app.main import app
    # Vercel procura por esta exportação
    __all__ = ["app"]
except Exception as e:
    print(f"ERROR importing app: {e}", file=sys.stderr)
    traceback.print_exc()
    raise
