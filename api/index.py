"""
Vercel Entrypoint

Este arquivo é o entrypoint para deploy no Vercel.
Exporta a aplicação FastAPI para o Vercel Serverless Functions.
"""

import sys
import os

# Garantir que o diretório raiz está no path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
except Exception as e:
    # Criar uma aplicação de fallback que mostra o erro
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import traceback

    app = FastAPI()

    error_details = {
        "error": str(e),
        "traceback": traceback.format_exc(),
        "python_path": sys.path,
        "cwd": os.getcwd()
    }

    @app.get("/{path:path}")
    async def error_handler(path: str):
        return JSONResponse(
            status_code=500,
            content=error_details
        )
