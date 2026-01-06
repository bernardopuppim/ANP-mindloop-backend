# 🧠 MindLoop Backend

Backend standalone para sistema de classificação de eventos SMS usando **LATS-P** (Language Agent Tree Search - Probabilistic) com **HITL** (Human-in-the-Loop).

---

## 📋 Sobre

API REST desenvolvida em **FastAPI** para classificação inteligente de eventos SMS da ANP (Agência Nacional do Petróleo).

Este projeto é **completamente independente**, sem frontend, pronto para deploy **serverless** (Vercel) ou **containerizado** (Docker/K8s).

---

## 🚀 Features

- ✅ **LATS-P**: Algoritmo de busca em árvore probabilística
- ✅ **HITL**: Human-in-the-loop com detecção de entropia
- ✅ **Serverless Mode**: Deploy otimizado para Vercel (< 250 MB)
- ✅ **Full Mode**: Modo completo com RAG/FAISS para ambientes locais
- ✅ **Configuração 100% ENV**: Sem dependência de `config.ini`
- ✅ **Logging Estruturado**: JSON logs para produção
- ✅ **CORS Configurável**: Integração com frontend
- ✅ **OpenAPI Docs**: Swagger UI automático

---

## 🏗️ Arquitetura

```
mindloop-backend/
├── app/
│   ├── main.py              # Aplicação FastAPI
│   ├── api/
│   │   ├── models.py        # Modelos Pydantic
│   │   └── routes.py        # Rotas da API
│   ├── core/
│   │   ├── config.py        # Configuração via ENV
│   │   ├── logging_setup.py # Setup de logging
│   │   └── errors.py        # Exception handlers
│   ├── services/
│   │   └── lats_service.py  # Lógica LATS-P
│   └── lats_sistema/        # Engine LATS completo
├── api/
│   └── index.py             # Entrypoint Vercel
├── requirements.txt         # Deps serverless
├── requirements-full.txt    # Deps full (RAG/FAISS)
├── .env.example             # Template de variáveis
├── vercel.json              # Config Vercel
└── README.md
```

---

## ⚙️ Configuração

### 1. Pré-requisitos

- **Python** 3.10+
- **pip** ou **uv**

### 2. Instalação

#### Modo Serverless (produção)

```bash
# Clone o repositório
git clone <seu-repositorio>
cd mindloop-backend

# Crie virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale dependências mínimas
pip install -r requirements.txt
```

#### Modo Full (desenvolvimento com RAG/FAISS)

```bash
# Instale dependências completas
pip install -r requirements-full.txt
```

### 3. Variáveis de Ambiente

Crie `.env` baseado em `.env.example`:

```bash
cp .env.example .env
```

**Configuração mínima (obrigatória)**:

```env
# .env
OPENAI_API_KEY=sk-proj-...
SERVERLESS_MODE=1
CORS_ORIGINS=http://localhost:3000
```

**Configuração completa**:

```env
# Runtime
ENV=development
DEBUG=false

# Modes
SERVERLESS_MODE=1     # 0 = full mode, 1 = serverless
FAST_MODE=0           # 0 = normal, 1 = economia de tokens

# OpenAI
OPENAI_API_KEY=sk-proj-...
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small

# Azure (opcional)
# AZURE_API_KEY=...
# AZURE_ENDPOINT=https://...

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Features
USE_HYDE=0
USE_RAG=0
SKIP_RAG_DEFAULT=1

# Logging
LOG_LEVEL=INFO
```

---

## 🏃 Executando Localmente

### Desenvolvimento

```bash
# Ativar virtual environment
source .venv/bin/activate

# Rodar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse:
- **API**: http://localhost:8000
- **Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Produção (local)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🌐 Deploy

### Vercel (Serverless)

#### Via Dashboard

1. Acesse [vercel.com](https://vercel.com)
2. Import repositório
3. Configure variáveis de ambiente:

```
SERVERLESS_MODE=1
OPENAI_API_KEY=sk-proj-...
OPENAI_CHAT_MODEL=gpt-4o-mini
CORS_ORIGINS=https://seu-frontend.vercel.app
```

4. Deploy

#### Via CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

**Importante**: O Vercel usa `api/index.py` como entrypoint.

---

### Docker

#### Modo Serverless

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY api/ ./api/

ENV SERVERLESS_MODE=1
ENV PYTHONPATH=.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t mindloop-backend .
docker run -p 8000:8000 --env-file .env mindloop-backend
```

#### Modo Full (com RAG)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements-full.txt .
RUN pip install --no-cache-dir -r requirements-full.txt

COPY app/ ./app/
COPY api/ ./api/

ENV SERVERLESS_MODE=0
ENV PYTHONPATH=.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### Outras Plataformas

**Railway**:
```bash
railway login
railway init
railway up
```

**Render**:
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**AWS Lambda** (via Mangum):
```python
# api/lambda_handler.py
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

---

## 📡 API Endpoints

### Health Check

```bash
GET /health
```

**Response**:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "mode": "serverless",
  "features": {
    "rag": false,
    "hyde": false,
    "serverless_mode": true,
    "fast_mode": false
  }
}
```

---

### Classificação de Evento

```bash
POST /predict
Content-Type: application/json

{
  "descricao_evento": "Vazamento de óleo no mar"
}
```

**Response (sem HITL)**:
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

**Response (com HITL)**:
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
  "state": {...}
}
```

---

### Continuação HITL

```bash
POST /hitl/continue
Content-Type: application/json

{
  "state": {...},
  "selected_child": "node_123",
  "justification": "Análise manual"
}
```

**Response**:
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

---

## 🔧 Modos de Operação

### Serverless Mode (`SERVERLESS_MODE=1`)

**Otimizado para Vercel/Lambda**:
- ❌ RAG/FAISS desabilitado
- ❌ Sem numpy/pandas
- ✅ LATS-P completo
- ✅ HITL completo
- ✅ Bundle < 100 MB
- ✅ Cold start ~2-3s

**Use quando**:
- Deploy em Vercel/Lambda
- Limite de bundle size
- Não precisa de busca vetorial

### Full Mode (`SERVERLESS_MODE=0`)

**Completo com RAG/FAISS**:
- ✅ RAG pipeline completo
- ✅ FAISS para busca vetorial
- ✅ Memória episódica
- ✅ HyDE (opcional)
- ⚠️ Bundle ~300-400 MB

**Use quando**:
- Ambiente local/container
- Precisa de RAG/contexto normativo
- Tem recursos suficientes

---

## 🧪 Testes

### Teste Manual

```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"descricao_evento": "Vazamento de óleo"}'
```

### Testes Automatizados

```bash
# Install dev dependencies
pip install pytest pytest-cov httpx

# Run tests
pytest tests/ -v

# Coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 🔍 Troubleshooting

### Erro: `ValidationError: OPENAI_API_KEY field required`

**Causa**: Variável de ambiente não configurada

**Solução**:
```bash
export OPENAI_API_KEY=sk-proj-...
# ou adicione no .env
```

---

### Erro: `ModuleNotFoundError: No module named 'faiss'`

**Causa**: Tentando usar RAG em serverless mode

**Solução**:
```env
# .env
SERVERLESS_MODE=1
USE_RAG=0
```

Ou instale dependências completas:
```bash
pip install -r requirements-full.txt
```

---

### Erro: `CORS policy blocked`

**Causa**: Frontend não está nas origins permitidas

**Solução**:
```env
# .env
CORS_ORIGINS=http://localhost:3000,https://seu-frontend.vercel.app
```

---

### Bundle size excede 250 MB no Vercel

**Causa**: Dependências pesadas instaladas

**Solução**:
1. Confirme `SERVERLESS_MODE=1` em `vercel.json`
2. Use `requirements.txt` (não `requirements-full.txt`)
3. Verifique `.vercelignore` está correto

---

## 📊 Métricas Esperadas

| Métrica | Serverless | Full |
|---------|-----------|------|
| **Bundle size** | ~80-100 MB | ~300-400 MB |
| **Cold start** | ~2-3s | ~5-10s |
| **Response time** | ~1-3s | ~2-5s |
| **Memory usage** | ~200-300 MB | ~500-800 MB |

---

## 🔗 Frontend

Este backend requer o frontend MindLoop para interface completa.

**Repositório**: [mindloop-frontend](https://github.com/seu-usuario/mindloop-frontend)

**Configurar no frontend**:
```env
# Frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📝 Licença

Este projeto é privado e proprietário.

---

## 👤 Autor

**Bernardo Puppim**

- GitHub: [@bernardopuppim](https://github.com/bernardopuppim)

---

## 🤝 Suporte

Para questões ou problemas:

1. Verifique os logs: `LOG_LEVEL=DEBUG`
2. Confirme variáveis de ambiente
3. Teste `/health` endpoint
4. Revise a documentação em `/docs`

---

**Status**: ✅ Produção pronto
**Versão**: 1.0.0
**Última atualização**: 2026-01-06
