"""
Exceções customizadas e error handlers.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class MindLoopError(Exception):
    """Base exception para erros do MindLoop"""

    def __init__(self, message: str, details: Dict[str, Any] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(MindLoopError):
    """Erro de configuração"""
    pass


class LATSExecutionError(MindLoopError):
    """Erro durante execução do LATS-P"""
    pass


class RAGError(MindLoopError):
    """Erro durante execução do RAG"""
    pass


# ==========================================
# Exception Handlers
# ==========================================

async def mindloop_error_handler(request: Request, exc: MindLoopError) -> JSONResponse:
    """Handler para erros do MindLoop"""
    logger.error(f"MindLoop Error: {exc.message}", extra={"details": exc.details})

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details
        }
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler para erros de validação"""
    logger.warning(f"Validation Error: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler genérico para exceções não tratadas"""
    logger.exception(f"Unhandled exception: {str(exc)}")

    # Em produção, não expor stacktrace
    from app.core.config import settings

    if settings().is_production:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred"
            }
        )
    else:
        # Em dev, mostrar detalhes
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc),
                "type": type(exc).__name__
            }
        )
