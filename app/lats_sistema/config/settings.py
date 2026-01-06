"""
Configuração do LATS Sistema.

100% baseado em variáveis de ambiente - SEM config.ini.
Compatível com o novo sistema de configuração centralizada.
"""

import os
import httpx
import logging

logger = logging.getLogger(__name__)

# ============================
# 🚀 MODO SERVERLESS/FULL
# ============================
# SERVERLESS_MODE substituiu SERVERLESS_FAST_MODE
SERVERLESS_FAST_MODE = os.getenv("SERVERLESS_MODE", "0") == "1"

# ============================
# OpenAI Configuration (via ENV)
# ============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

# ============================
# Azure Configuration (via ENV - opcional)
# ============================
AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2025-01-01-preview")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "")
AZURE_CA_CERT_PATH = ""  # Não usado no novo sistema

# ============================
# Logging
# ============================
if SERVERLESS_FAST_MODE:
    logger.info("[SERVERLESS MODE] Memória episódica (FAISS) desabilitada")
    logger.info("[CONFIG] Modo serverless - usando variáveis de ambiente")
else:
    logger.info("[CONFIG] Modo full - RAG/FAISS habilitados")
    logger.info("[CONFIG] Usando variáveis de ambiente")

# ============================
# Cliente HTTP (simplificado)
# ============================
def get_http_client():
    """
    Retorna cliente HTTP padrão.

    No novo sistema, não usamos certificados customizados.
    """
    return httpx.Client()
