"""
MindLoop Backend - FastAPI Application

Sistema de classificação de eventos SMS usando LATS-P (Language Agent Tree Search).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import logging

from app.core.config import settings
from app.core.logging_setup import setup_logging
from app.core.errors import (
    MindLoopError,
    mindloop_error_handler,
    validation_error_handler,
    generic_error_handler
)
from app.api.routes import router

# ============================================================================
# Configurar Logging
# ============================================================================
config = settings()
setup_logging(
    level=config.log_level,
    json_format=config.is_production
)

logger = logging.getLogger(__name__)

# ============================================================================
# Criar Aplicação FastAPI
# ============================================================================

app = FastAPI(
    title="MindLoop Backend API",
    description="Sistema de classificação de eventos SMS usando LATS-P",
    version="1.0.0",
    docs_url="/docs" if not config.is_production else None,  # Desabilitar docs em prod
    redoc_url="/redoc" if not config.is_production else None
)

# ============================================================================
# CORS Middleware
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured for origins: {config.cors_origins_list}")

# ============================================================================
# Exception Handlers
# ============================================================================

app.add_exception_handler(MindLoopError, mindloop_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# ============================================================================
# Register Routers
# ============================================================================

app.include_router(router)

# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Executado ao iniciar a aplicação.

    Exibe informações sobre a configuração.
    """
    logger.info("=" * 70)
    logger.info(" 🚀 MINDLOOP BACKEND STARTED")
    logger.info("=" * 70)
    logger.info(f"Environment: {config.env}")
    logger.info(f"Mode: {'serverless' if config.is_serverless else 'full'}")
    logger.info(f"Debug: {config.debug}")
    logger.info(f"CORS Origins: {config.cors_origins_list}")
    logger.info("=" * 70)
    logger.info(" 📝 Available endpoints:")
    logger.info("   GET  /")
    logger.info("   GET  /health")
    logger.info("   POST /predict")
    logger.info("   POST /hitl/continue")
    if not config.is_production:
        logger.info("   GET  /docs (Swagger UI)")
        logger.info("   GET  /redoc (ReDoc)")
    logger.info("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """Executado ao desligar a aplicação"""
    logger.info("Shutting down MindLoop Backend...")


# ============================================================================
# Root Endpoint (compatibility)
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {"status": "ok", "message": "MindLoop Backend API - Use /docs for documentation"}
