# ⚡ Quick Start - MindLoop Backend

## 🏃 Rodar Agora (Local)

```bash
cd /home/puppyn/projects/mindloop-backend

# Criar venv
python -m venv .venv
source .venv/bin/activate

# Instalar deps
pip install -r requirements.txt

# Configurar ENV
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY

# Rodar
uvicorn app.main:app --reload --port 8000
```

**URL**: http://localhost:8000
**Docs**: http://localhost:8000/docs

---

## 🌐 Deploy Vercel (1 minuto)

```bash
# Login
vercel login

# Deploy
vercel --prod
```

Configure no dashboard:
```
SERVERLESS_MODE=1
OPENAI_API_KEY=sk-proj-...
CORS_ORIGINS=https://seu-frontend.vercel.app
```

---

## 🧪 Testar API

```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"descricao_evento": "Vazamento de óleo no mar"}'
```

---

## 📁 Arquivos Importantes

- [README.md](README.md) - Documentação completa
- [.env.example](.env.example) - Template de variáveis
- [app/main.py](app/main.py) - Aplicação FastAPI
- [app/core/config.py](app/core/config.py) - Configuração

---

## 🐛 Problemas Comuns

### "ValidationError: OPENAI_API_KEY field required"
**Solução**: Configure `.env` com sua chave OpenAI

### "CORS policy blocked"
**Solução**: Adicione URL do frontend em `CORS_ORIGINS`

### "ModuleNotFoundError: No module named 'faiss'"
**Solução**: Confirme `SERVERLESS_MODE=1` no `.env`

---

**Tudo pronto!** 🎉
