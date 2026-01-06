"""
Modelos Pydantic para API requests/responses.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class PredictRequest(BaseModel):
    """Request para classificação de evento"""

    # Campo principal esperado pelo frontend
    texto_evento: str = Field(
        ...,
        alias="descricao_evento",
        description="Descrição do evento SMS a ser classificado"
    )

    # Campos opcionais
    contexto_normativo: Optional[str] = Field(
        default=None,
        description="Contexto normativo adicional (opcional)"
    )

    state: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Estado do grafo LATS (para continuação)"
    )

    class Config:
        populate_by_name = True


class HitlContinueRequest(BaseModel):
    """Request para continuação após HITL (Human-in-the-Loop)"""

    state: Dict[str, Any] = Field(
        ...,
        description="Estado do grafo LATS salvo"
    )

    selected_child: str = Field(
        ...,
        description="ID do nó filho selecionado pelo humano"
    )

    justification: Optional[str] = Field(
        default=None,
        description="Justificativa fornecida pelo humano (opcional)"
    )


class PredictResponse(BaseModel):
    """Response da classificação"""

    hitl_required: bool = Field(
        ...,
        description="Indica se intervenção humana é necessária"
    )

    state: Dict[str, Any] = Field(
        ...,
        description="Estado completo do grafo"
    )

    hitl_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metadados para modal HITL (opções, probabilidades, etc)"
    )

    final: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Resultado final da classificação (quando completo)"
    )

    confianca: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Métricas de confiança (deprecated - usar resultado_formatado)"
    )

    resultado_formatado: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Saída formatada para UI"
    )


class HealthResponse(BaseModel):
    """Response do health check"""

    status: str = Field(default="ok")
    version: str = Field(default="1.0.0")
    mode: str = Field(..., description="Runtime mode (serverless/full)")
    features: Dict[str, bool] = Field(
        ...,
        description="Feature flags ativos"
    )
