# Sistema de Notificações Toast

Sistema de notificações inspirado no sistema de flash messages do projeto CaseBem.

## Componentes

### 1. Backend (Python)

#### `util/toast_messages.py`
Gerencia as notificações toast no backend:

```python
from util.toast_messages import toast_sucesso, toast_erro, toast_aviso, toast_info, toast_validacao_erro

# Toast de sucesso
toast_sucesso(request, "Operação realizada com sucesso!")

# Toast de erro
toast_erro(request, "Erro ao processar requisição")

# Toast de aviso
toast_aviso(request, "Atenção: verifique os dados")

# Toast de informação
toast_info(request, "Processamento iniciado")

# Toast com erros de validação (múltiplos erros)
erros = ["Nome é obrigatório", "Email inválido"]
toast_validacao_erro(request, erros)
```

#### `util/dto_error_handler.py`
Converte erros de validação do Pydantic em mensagens toast:

```python
from pydantic import ValidationError
from util.dto_error_handler import tratar_erro_validacao

try:
    dto = CriarProdutoDTO(**form_data)
except ValidationError as e:
    erros = tratar_erro_validacao(request, e)
    # Erros já foram convertidos em toast automaticamente
```

#### `util/template_util.py`
Injeta toasts automaticamente em todos os templates através do context processor.

#### `middleware/toast_middleware.py`
Middleware para processamento de toasts (atualmente não utilizado, pois a injeção é feita via context processor).

### 2. Frontend

#### `static/js/toast.js`
Gerenciador de toasts JavaScript:

```javascript
// Uso manual no JavaScript
toast.success("Operação realizada!");
toast.error("Erro ao processar");
toast.warning("Atenção!");
toast.info("Informação importante");

// Toasts do servidor são processados automaticamente
```

#### `static/css/toast.css`
Estilos para os toasts com cores diferenciadas por tipo:
- **Sucesso**: Verde
- **Erro**: Vermelho
- **Aviso**: Amarelo
- **Info**: Azul

### 3. Templates

#### `templates/base.html`
Template base atualizado para incluir:
- Link para `toast.css`
- Script para `toast.js`
- Injeção automática de toasts do servidor

## Como Usar

### Em uma Rota FastAPI

```python
from fastapi import APIRouter, Request
from util.toast_messages import toast_sucesso, toast_erro

@router.post("/cadastrar")
async def post_cadastrar(request: Request, produto_dto: CriarProdutoDTO):
    try:
        # Processar dados
        produto_id = produto_repo.inserir(produto)

        if produto_id:
            toast_sucesso(request, "Produto cadastrado com sucesso!")
            return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
        else:
            toast_erro(request, "Erro ao cadastrar produto")
            return templates.TemplateResponse("cadastrar.html", {"request": request})
    except Exception as e:
        toast_erro(request, f"Erro inesperado: {str(e)}")
        return templates.TemplateResponse("cadastrar.html", {"request": request})
```

### Com Validação de DTOs

Os toasts funcionam automaticamente com a validação do Pydantic. Quando um DTO falha na validação, os erros são automaticamente convertidos em toast:

```python
@router.post("/cadastrar")
async def post_cadastrar(request: Request, produto_dto: CriarProdutoDTO):
    # Se produto_dto tiver erros de validação, FastAPI automaticamente retorna 422
    # Para capturar e converter em toast:

    produto_id = produto_repo.inserir(produto_dto)
    toast_sucesso(request, "Produto cadastrado!")
    return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)
```

### No JavaScript (Frontend)

```javascript
// Toasts do servidor são exibidos automaticamente quando a página carrega

// Para toasts manuais:
document.getElementById('meuBotao').addEventListener('click', () => {
    toast.success('Ação realizada com sucesso!');
});
```

## Tipos de Toast

| Tipo | Função | Cor | Ícone | Duração Padrão |
|------|--------|-----|-------|----------------|
| Sucesso | `toast_sucesso()` | Verde | ✓ | 5s |
| Erro | `toast_erro()` | Vermelho | ✗ | 5s |
| Aviso | `toast_aviso()` | Amarelo | ⚠ | 5s |
| Info | `toast_info()` | Azul | ℹ | 5s |
| Validação | `toast_validacao_erro()` | Vermelho | ✗ | 7s |

## Personalização

### Duração Customizada

```python
toast_sucesso(request, "Mensagem", duration=10000)  # 10 segundos
```

### Título Customizado

```python
toast_erro(request, "Mensagem de erro", title="Ops!")
```

### Toast com HTML (para listas de erros)

```python
erros = ["Erro 1", "Erro 2", "Erro 3"]
toast_validacao_erro(request, erros)  # Automaticamente formata como lista HTML
```

## Arquivos Modificados

- `templates/base.html` - Adicionado suporte a toasts
- `util/template_util.py` - Injeção de toasts via context processor
- `routes/admin_categorias_routes.py` - Exemplo de integração

## Arquivos Criados

- `util/toast_messages.py` - Sistema de toasts backend
- `util/dto_error_handler.py` - Tratamento de erros de validação
- `middleware/toast_middleware.py` - Middleware (opcional)
- `static/js/toast.js` - JavaScript para toasts
- `static/css/toast.css` - Estilos dos toasts
- `TOAST_SYSTEM.md` - Esta documentação

## Exemplo Completo

```python
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from util.toast_messages import toast_sucesso, toast_erro, toast_aviso

router = APIRouter()

@router.post("/processar")
async def processar(request: Request, dados: DadosDTO):
    # Validação de negócio
    if not validar_dados(dados):
        toast_aviso(request, "Alguns dados precisam de atenção")
        return templates.TemplateResponse("form.html", {"request": request, "dados": dados})

    # Processar
    try:
        resultado = processar_dados(dados)
        toast_sucesso(request, "Dados processados com sucesso!")
        return RedirectResponse("/sucesso", status.HTTP_303_SEE_OTHER)
    except Exception as e:
        toast_erro(request, f"Erro ao processar: {str(e)}")
        return templates.TemplateResponse("form.html", {"request": request, "dados": dados})
```

## Notas

- Os toasts são armazenados na sessão e exibidos apenas uma vez (padrão flash message)
- Após serem exibidos, os toasts são automaticamente removidos da sessão
- Múltiplos toasts podem ser exibidos simultaneamente
- Toasts são responsivos e se adaptam a telas pequenas
- Bootstrap 5 é necessário para o funcionamento dos toasts
- Bootstrap Icons é usado para os ícones dos toasts
