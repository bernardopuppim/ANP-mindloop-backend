# Fix: CORS Configuration for Production - Resolvido ✅

**Data**: 2026-01-09
**Problema**: "Failed to fetch" devido a CORS bloqueando requisições do frontend
**Status**: ✅ **RESOLVIDO E VALIDADO**

---

## 🐛 Problema Identificado

### Erro no Frontend
```
Erro ao classificar: Failed to fetch
```

### Erro no Backend (CORS Preflight)
```bash
$ curl -X OPTIONS https://mindloop-backend.vercel.app/predict \
  -H "Origin: https://projeto-anp.mindloop.ia.br"

HTTP/2 400
Disallowed CORS origin
```

---

## 🔍 Causa Raiz

### Configuração CORS Incompleta

O backend FastAPI está configurado para aceitar requisições CORS via variável de ambiente `CORS_ORIGINS`:

```python
# app/core/config.py
cors_origins: str = Field(
    default="http://localhost:3000,http://localhost:3001",
    alias="CORS_ORIGINS"
)
```

**Problema**: A variável `CORS_ORIGINS` no Vercel estava configurada **apenas com URLs de localhost**, não incluindo a URL de produção `https://projeto-anp.mindloop.ia.br`.

### Por que causava "Failed to fetch"?

1. **Browser faz preflight request** (OPTIONS)
2. **Backend verifica origin** contra `CORS_ORIGINS`
3. **Origin não está na lista** → Backend retorna 400 "Disallowed CORS origin"
4. **Browser bloqueia requisição** → Frontend recebe "Failed to fetch"

---

## ✅ Solução Implementada

### 1. Remover Variável Antiga
```bash
vercel env rm CORS_ORIGINS production --yes
```

### 2. Adicionar com URLs de Produção
```bash
echo "http://localhost:3000,http://localhost:3001,https://projeto-anp.mindloop.ia.br,https://mindloop-frontend-bernardos-projects-2a2b13bb.vercel.app" | \
  vercel env add CORS_ORIGINS production
```

**Valor configurado**:
```
http://localhost:3000,http://localhost:3001,https://projeto-anp.mindloop.ia.br,https://mindloop-frontend-bernardos-projects-2a2b13bb.vercel.app
```

### 3. Redeploy do Backend
```bash
vercel --prod --yes
```

**Output**:
```
✓ Build Completed in /vercel/output [5s]
✓ Deployment completed
✓ Aliased: https://mindloop-backend.vercel.app
```

---

## 🧪 Validação

### Teste CORS Preflight

**Antes** (❌ Bloqueado):
```bash
$ curl -X OPTIONS https://mindloop-backend.vercel.app/predict \
  -H "Origin: https://projeto-anp.mindloop.ia.br"

HTTP/2 400
Disallowed CORS origin
```

**Depois** (✅ Permitido):
```bash
$ curl -X OPTIONS https://mindloop-backend.vercel.app/predict \
  -H "Origin: https://projeto-anp.mindloop.ia.br"

HTTP/2 200
access-control-allow-origin: https://projeto-anp.mindloop.ia.br
access-control-allow-credentials: true
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
access-control-allow-headers: content-type
```

### Teste POST Real

```bash
$ curl -X POST https://mindloop-backend.vercel.app/predict \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://projeto-anp.mindloop.ia.br' \
  -d '{"descricao_evento": "Trabalhador escorregou em chão molhado"}'
```

**Resultado**: ✅ `{"hitl_required":true, ...}` (resposta válida)

### Testes Automatizados

```bash
$ ./final-validation-test.sh
```

**Resultados**:
```
1️⃣  Backend Health Check
✅ Backend is healthy

2️⃣  Backend CORS Configuration
✅ CORS is configured
   access-control-allow-origin: https://projeto-anp.mindloop.ia.br

3️⃣  Testing /predict Endpoint
✅ Backend /predict is working
   📋 HITL was triggered (as expected for ambiguous events)

4️⃣  Frontend Deployment Check
✅ Frontend is deployed with LoopynSMS branding

5️⃣  JavaScript Bundle Configuration
✅ Frontend is configured with production backend URL

🎉 All tests passed!
```

---

## 📊 Comparação: Antes vs Depois

| Aspecto | ❌ Antes | ✅ Depois |
|---------|----------|-----------|
| **CORS Preflight** | 400 Disallowed | ✅ 200 OK |
| **Access-Control-Allow-Origin** | Not set | ✅ https://projeto-anp.mindloop.ia.br |
| **Frontend → Backend** | Failed to fetch | ✅ Working |
| **CORS_ORIGINS value** | localhost only | ✅ Includes production URLs |
| **Browser Console** | CORS error | ✅ No errors |

---

## 🔄 Como Funciona o CORS

### 1. Browser Faz Preflight Request
```http
OPTIONS /predict HTTP/1.1
Host: mindloop-backend.vercel.app
Origin: https://projeto-anp.mindloop.ia.br
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
```

### 2. Backend Verifica Origin
```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins_list,  # ← Verifica aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Backend Responde
```http
HTTP/2 200
access-control-allow-origin: https://projeto-anp.mindloop.ia.br
access-control-allow-credentials: true
access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
access-control-allow-headers: content-type
```

### 4. Browser Permite Request Real
```http
POST /predict HTTP/1.1
Host: mindloop-backend.vercel.app
Origin: https://projeto-anp.mindloop.ia.br
Content-Type: application/json
```

---

## 🎯 Lições Aprendidas

### 1. CORS Precisa Incluir Todas as URLs de Produção
- ❌ **Errado**: Apenas localhost
- ✅ **Correto**: Localhost + todas URLs de produção

### 2. Variáveis de Ambiente Requerem Redeploy
- Mudanças em env vars não afetam deploys existentes
- Sempre fazer redeploy após alterar configuração

### 3. Testar CORS com OPTIONS Request
```bash
curl -X OPTIONS <api-url> \
  -H "Origin: <frontend-url>" \
  -H "Access-Control-Request-Method: POST"
```

### 4. Browser Console Mostra Erros CORS
- Sempre verificar console (F12) para erros de CORS
- Mensagens indicam claramente bloqueio de CORS

---

## 📝 Checklist de CORS para Novos Domínios

Quando adicionar novo domínio frontend:

- [ ] Identificar todas URLs (produção, preview, aliases)
- [ ] Adicionar à variável `CORS_ORIGINS`
- [ ] Fazer redeploy do backend
- [ ] Testar preflight request com curl
- [ ] Testar POST request real
- [ ] Verificar no browser console (sem erros CORS)
- [ ] Validar com testes automatizados

---

## 🚀 Configuração Atual

### Variável de Ambiente (Vercel)
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://projeto-anp.mindloop.ia.br,https://mindloop-frontend-bernardos-projects-2a2b13bb.vercel.app
```

### URLs Permitidas
1. ✅ `http://localhost:3000` - Desenvolvimento local
2. ✅ `http://localhost:3001` - Desenvolvimento alternativo
3. ✅ `https://projeto-anp.mindloop.ia.br` - Produção (domínio custom)
4. ✅ `https://mindloop-frontend-bernardos-projects-2a2b13bb.vercel.app` - Vercel URL

---

## 📚 Comandos Úteis

### Verificar CORS Atual
```bash
# Testar preflight
curl -i -X OPTIONS https://mindloop-backend.vercel.app/predict \
  -H "Origin: https://projeto-anp.mindloop.ia.br" \
  -H "Access-Control-Request-Method: POST"

# Deve retornar 200 com headers access-control-allow-*
```

### Listar Variáveis de Ambiente
```bash
vercel env ls
```

### Atualizar CORS
```bash
# Remover antiga
vercel env rm CORS_ORIGINS production --yes

# Adicionar nova
echo "<origins-separated-by-comma>" | vercel env add CORS_ORIGINS production

# Redeploy
vercel --prod --yes
```

### Verificar Logs
```bash
vercel logs mindloop-backend.vercel.app
```

---

## 🎊 Status Final

### Backend
- ✅ **CORS configurado** para produção
- ✅ **Preflight requests** retornam 200
- ✅ **POST requests** funcionando
- ✅ **Logs** sem erros de CORS

### Frontend
- ✅ **Requisições permitidas** pelo browser
- ✅ **Console limpo** (sem erros CORS)
- ✅ **Classificação funcionando**
- ✅ **HITL operacional**

### Integração
- ✅ **Frontend ↔ Backend** comunicando
- ✅ **Todos os testes** passando
- ✅ **Sistema operacional** em produção

---

## 🔗 Links Relacionados

- **Frontend**: https://projeto-anp.mindloop.ia.br
- **Backend**: https://mindloop-backend.vercel.app
- **Backend Docs**: https://mindloop-backend.vercel.app/docs

---

## 📖 Documentação Relacionada

1. **[BUILD_FIX_SUMMARY.md](../mindloop-frontend/BUILD_FIX_SUMMARY.md)** - Fix do build TypeScript
2. **[FIX_ENV_VARIABLE_NEWLINE.md](../mindloop-frontend/FIX_ENV_VARIABLE_NEWLINE.md)** - Fix da variável NEXT_PUBLIC_API_URL
3. **[FIX_CORS_PRODUCTION.md](FIX_CORS_PRODUCTION.md)** - Este documento
4. **[TROUBLESHOOTING.md](../mindloop-frontend/TROUBLESHOOTING.md)** - Guia geral

---

**Data do Fix**: 2026-01-09
**Tempo para Resolver**: ~15 minutos
**Status**: ✅ **RESOLVIDO E VALIDADO**
**Sistema**: ✅ **Operacional em Produção**
