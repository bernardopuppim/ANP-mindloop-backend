"""
Configuração centralizada via variáveis de ambiente.

SEM dependência de config.ini - tudo via ENV vars.
"""

import os
import logging
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Configurações da aplicação via variáveis de ambiente.

    Todas as variáveis têm defaults seguros para desenvolvimento local.
    Apenas OPENAI_API_KEY é obrigatória (fail-fast se não fornecida).
    """

    # ==========================================
    # Runtime Environment
    # ==========================================
    env: str = Field(default="development", alias="ENV")
    debug: bool = Field(default=False, alias="DEBUG")

    # ==========================================
    # Mode Flags
    # ==========================================
    serverless_mode: bool = Field(default=False, alias="SERVERLESS_MODE")
    fast_mode: bool = Field(default=False, alias="FAST_MODE")

    # ==========================================
    # OpenAI Configuration
    # ==========================================
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")  # Obrigatório
    openai_chat_model: str = Field(default="gpt-4o-mini", alias="OPENAI_CHAT_MODEL")
    openai_embed_model: str = Field(default="text-embedding-3-small", alias="OPENAI_EMBED_MODEL")

    # ==========================================
    # Azure Configuration (Optional)
    # ==========================================
    azure_api_key: Optional[str] = Field(default=None, alias="AZURE_API_KEY")
    azure_endpoint: Optional[str] = Field(default=None, alias="AZURE_ENDPOINT")
    azure_api_version: str = Field(default="2025-01-01-preview", alias="AZURE_API_VERSION")
    azure_deployment_name: Optional[str] = Field(default=None, alias="AZURE_DEPLOYMENT_NAME")

    # ==========================================
    # CORS Configuration
    # ==========================================
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:3001",
        alias="CORS_ORIGINS"
    )

    # ==========================================
    # Feature Flags
    # ==========================================
    use_hyde: bool = Field(default=False, alias="USE_HYDE")
    use_rag: bool = Field(default=False, alias="USE_RAG")
    skip_rag_default: bool = Field(default=True, alias="SKIP_RAG_DEFAULT")

    # ==========================================
    # Logging
    # ==========================================
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        populate_by_name = True

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string into list"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.env.lower() in ("production", "prod")

    @property
    def is_serverless(self) -> bool:
        """Check if running in serverless mode"""
        return self.serverless_mode


# ==========================================
# Global Settings Instance
# ==========================================
def get_settings() -> Settings:
    """
    Retorna instância de configurações.

    Fail-fast se OPENAI_API_KEY não estiver definida.
    """
    try:
        settings = Settings()

        # Log startup info
        logger.info("=" * 70)
        logger.info(" 🚀 MINDLOOP BACKEND - CONFIGURATION LOADED")
        logger.info("=" * 70)
        logger.info(f"Environment: {settings.env}")
        logger.info(f"Debug: {settings.debug}")
        logger.info(f"Serverless Mode: {settings.is_serverless}")
        logger.info(f"Fast Mode: {settings.fast_mode}")
        logger.info(f"OpenAI Model: {settings.openai_chat_model}")
        logger.info(f"Embedding Model: {settings.openai_embed_model}")
        logger.info(f"Use HyDE: {settings.use_hyde}")
        logger.info(f"Use RAG: {settings.use_rag}")
        logger.info(f"Skip RAG Default: {settings.skip_rag_default}")
        logger.info(f"CORS Origins: {settings.cors_origins_list}")
        logger.info(f"Log Level: {settings.log_level}")

        if settings.azure_api_key:
            logger.info(f"Azure Endpoint: {settings.azure_endpoint}")
            logger.info(f"Azure Deployment: {settings.azure_deployment_name}")

        logger.info("=" * 70)

        return settings

    except Exception as e:
        logger.error("=" * 70)
        logger.error(" ❌ CONFIGURATION ERROR")
        logger.error("=" * 70)
        logger.error(f"Failed to load settings: {e}")
        logger.error("")
        logger.error("REQUIRED:")
        logger.error("  - OPENAI_API_KEY")
        logger.error("")
        logger.error("OPTIONAL:")
        logger.error("  - ENV (default: development)")
        logger.error("  - SERVERLESS_MODE (default: 0)")
        logger.error("  - OPENAI_CHAT_MODEL (default: gpt-4o-mini)")
        logger.error("  - CORS_ORIGINS (default: http://localhost:3000)")
        logger.error("=" * 70)
        raise


# Singleton instance
_settings: Optional[Settings] = None


def settings() -> Settings:
    """Get cached settings instance"""
    global _settings
    if _settings is None:
        _settings = get_settings()
    return _settings
