from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from dtos.categoria_dto import AlterarCategoriaDTO, CriarCategoriaDTO
from model.categoria_model import Categoria
from repo import categoria_repo
from util.flash_messages import informar_erro, informar_sucesso
from util.template_util import criar_templates
from util.auth_decorator import requer_autenticacao


router = APIRouter()
templates = criar_templates("templates/admin/categorias")

@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    categorias = categoria_repo.obter_todos()
    response = templates.TemplateResponse(
        "listar.html", {"request": request, "categorias": categorias}
    )
    return response


@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request, 
    nome: str = Form(...),
    usuario_logado: dict = None):
    # guarda os dados originais do formulário
    dados_formulario = {
        "nome": nome
    }
    try:
        # Validar dados com Pydantic
        dados = CriarCategoriaDTO(nome=nome)
        # Criar objeto Categoria
        nova_categoria = Categoria(id=0, nome=dados.nome)
        # Processar cadastro
        categoria_repo.inserir(nova_categoria)
        # Sucesso - Redirecionar com mensagem flash
        informar_sucesso(request, f"Categoria cadastrada com sucesso!")
        return RedirectResponse("/admin/categorias", status_code=303)
    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            erros.append(f"{campo.capitalize()}: {mensagem}")
        erro_msg = " | ".join(erros)
        # logger.warning(f"Erro de validação no cadastro: {erro_msg}")
        # Retornar template com dados preservados e erro
        informar_erro(request, "Há erros no formulário.")
        return templates.TemplateResponse("cadastrar.html", {
            "request": request,
            "erro": erro_msg,
            "dados": dados_formulario  # Preservar dados digitados
        })
    except Exception as e:
        # logger.error(f"Erro ao processar cadastro: {e}")
        return templates.TemplateResponse("cadastrar.html", {
            "request": request,
            "erro": "Erro ao processar cadastro. Tente novamente.",
            "dados": dados_formulario
        })


@router.get("/alterar/{id}")
@requer_autenticacao(["admin"])
async def get_alterar(request: Request, id: int, usuario_logado: dict = None):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "alterar.html", {"request": request, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/alterar")
@requer_autenticacao(["admin"])
async def post_alterar(
    request: Request, 
    categoria_dto: AlterarCategoriaDTO, 
    usuario_logado: dict = None):
    categoria = Categoria(id=categoria_dto.id, nome=categoria_dto.nome)
    if categoria_repo.atualizar(categoria):
        response = RedirectResponse(
            "/admin/categorias", status_code=status.HTTP_303_SEE_OTHER
        )
        return response
    return templates.TemplateResponse(
        "alterar.html",
        {"request": request, "mensagem": "Erro ao alterar categoria."},
    )


@router.get("/excluir/{id}")
@requer_autenticacao(["admin"])
async def get_excluir(request: Request, id: int, usuario_logado: dict = None):
    categoria = categoria_repo.obter_por_id(id)
    if categoria:
        response = templates.TemplateResponse(
            "excluir.html", {"request": request, "categoria": categoria}
        )
        return response
    return RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)


@router.post("/excluir")
@requer_autenticacao(["admin"])
async def post_excluir(request: Request, id: int = Form(...), usuario_logado: dict = None):
    if categoria_repo.excluir_por_id(id):
        response = RedirectResponse("/admin/categorias", status.HTTP_303_SEE_OTHER)
        return response
    return templates.TemplateResponse(
        "excluir.html",
        {"request": request, "mensagem": "Erro ao excluir categoria."},
    )
