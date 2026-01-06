"""
Configuração centralizada de logging.

Substitui prints por logging estruturado.
"""

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", json_format: bool = False) -> None:
    """
    Configura logging para toda a aplicação.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Se True, usa formato JSON (melhor para produção)
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Formato de log
    if json_format:
        # Formato JSON para produção (parsing fácil)
        log_format = '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","message":"%(message)s"}'
    else:
        # Formato legível para desenvolvimento
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configurar root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True  # Override any existing config
    )

    # Reduzir verbosidade de libs externas
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - Level: {level}")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get logger instance.

    Args:
        name: Logger name (usar __name__ do módulo)

    Returns:
        Logger instance
    """
    return logging.getLogger(name or __name__)
