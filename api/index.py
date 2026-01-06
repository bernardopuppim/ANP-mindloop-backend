"""
Vercel Entrypoint

Este arquivo é o entrypoint para deploy no Vercel.
Simplesmente exporta a aplicação FastAPI.
"""

from app.main import app

# Vercel procura por esta exportação
__all__ = ["app"]
