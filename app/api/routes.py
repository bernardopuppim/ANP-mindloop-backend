"""
Rotas da API.
"""

from fastapi import APIRouter, status
import logging

from app.api.models import (
    PredictRequest,
    HitlContinueRequest,
    PredictResponse,
    HealthResponse
)
from app.services.lats_service import executar_primeira_fase, continuar_pos_hitl
from app.core.config import settings

logger = logging.getLogger(__name__)

# Router principal
router = APIRouter()


# ============================================================================
# Health Check
# ============================================================================

@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Health check endpoint"
)
async def health_check():
    """
    Verifica o status do serviço.

    Retorna informações sobre o modo de execução e features ativas.
    """
    config = settings()

    return HealthResponse(
        status="ok",
        version="1.0.0",
        mode="serverless" if config.is_serverless else "full",
        features={
            "rag": config.use_rag,
            "hyde": config.use_hyde,
            "serverless_mode": config.is_serverless,
            "fast_mode": config.fast_mode
        }
    )


@router.get(
    "/",
    tags=["health"],
    summary="Root endpoint"
)
async def root():
    """Endpoint raiz - redireciona para health"""
    return {"status": "ok", "message": "MindLoop Backend API"}


# ============================================================================
# Classificação de Eventos
# ============================================================================

@router.post(
    "/predict",
    response_model=PredictResponse,
    status_code=status.HTTP_200_OK,
    tags=["classification"],
    summary="Classifica evento SMS"
)
async def predict(req: PredictRequest):
    """
    Classifica um evento SMS usando o algoritmo LATS-P.

    **Fluxo**:
    1. Executa pipeline RAG (se habilitado)
    2. Executa LATS-P com heurísticas e poda
    3. Avalia entropia da decisão
    4. Se entropia alta → retorna `hitl_required=True`
    5. Se entropia baixa → retorna classificação final

    **HITL (Human-in-the-Loop)**:
    - Quando `hitl_required=True`, o frontend deve mostrar modal
    - Modal exibe opções disponíveis (em `hitl_metadata`)
    - Usuário seleciona categoria e opcionalmente fornece justificativa
    - Envia requisição para `/hitl/continue` com escolha

    **Exemplo de Request**:
    ```json
    {
      "descricao_evento": "Vazamento de óleo no mar",
      "contexto_normativo": "...",  // opcional
      "state": {...}                // opcional (para continuação)
    }
    ```

    **Exemplo de Response (HITL não requerido)**:
    ```json
    {
      "hitl_required": false,
      "final": {
        "categoria_final": "Ambiental",
        "justificativa": "...",
        "log_prob": -0.5
      },
      "confianca": {...},
      "resultado_formatado": {...},
      "state": {...}
    }
    ```

    **Exemplo de Response (HITL requerido)**:
    ```json
    {
      "hitl_required": true,
      "hitl_metadata": {
        "opcoes": [
          {"id": "node_123", "label": "Ambiental", "prob": 0.35},
          {"id": "node_124", "label": "Operacional", "prob": 0.33}
        ],
        "entropia": 1.45
      },
      "state": {...}  // checkpoint completo
    }
    ```
    """
    logger.info(f"POST /predict - Evento: {req.texto_evento[:50]}...")
    return executar_primeira_fase(req)


# ============================================================================
# Continuação após HITL
# ============================================================================

@router.post(
    "/hitl/continue",
    response_model=PredictResponse,
    status_code=status.HTTP_200_OK,
    tags=["classification"],
    summary="Continua classificação após decisão humana"
)
async def hitl_continue(req: HitlContinueRequest):
    """
    Continua a classificação após intervenção humana (HITL).

    **Fluxo**:
    1. Recebe estado salvo + escolha do usuário
    2. Retoma execução do LATS-P a partir do checkpoint
    3. Aplica decisão humana ao grafo
    4. Continua até conclusão
    5. Retorna resultado final

    **Exemplo de Request**:
    ```json
    {
      "state": {...},                    // Estado salvo do /predict
      "selected_child": "node_123",      // ID do nó escolhido
      "justification": "Análise manual"  // Opcional
    }
    ```

    **Exemplo de Response**:
    ```json
    {
      "hitl_required": false,
      "final": {
        "categoria_final": "Ambiental",
        "justificativa": "Análise manual",
        "log_prob": -0.3
      },
      "confianca": {...},
      "resultado_formatado": {...},
      "state": {...}
    }
    ```
    """
    logger.info(f"POST /hitl/continue - Escolha: {req.selected_child}")
    return continuar_pos_hitl(req)
