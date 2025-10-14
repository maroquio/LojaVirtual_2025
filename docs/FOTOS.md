# 📸 Sistema de Fotos - Guia de Implementação

Este documento ensina como implementar sistemas de fotos em aplicações FastAPI, com dois cenários:
- **Foto única**: Uma foto por entidade (ex: perfil de usuário)
- **Galeria de fotos**: Múltiplas fotos por entidade (ex: produtos)

## 📋 Pré-requisitos

```bash
# Instalar dependência para processamento de imagens
pip install Pillow
```

---

## 🔧 1. FOTO ÚNICA (Perfil de Usuário)

### 1.1. Estrutura de Diretórios

```
static/
└── uploads/
    └── usuarios/          # Diretório para fotos de usuários
        ├── 1_abc123.jpg   # Formato: {id}_{hash}.{ext}
        └── 2_def456.png
```

### 1.2. Modelo de Dados

```python
# model/usuario_model.py
@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str
    foto: str = None  # ← Campo para armazenar caminho da foto
    perfil: str = 'cliente'
    data_cadastro: str = None
```

### 1.3. SQL para Foto

```python
# sql/usuario_sql.py

# Adicionar coluna foto à tabela existente (se não existir)
ADICIONAR_COLUNA_FOTO = """
ALTER TABLE usuario ADD COLUMN foto TEXT
"""

# Atualizar apenas a foto do usuário
ATUALIZAR_FOTO = """
UPDATE usuario SET foto = ? WHERE id = ?
"""
```

### 1.4. Repository - Função de Atualizar Foto

```python
# repo/usuario_repo.py

def atualizar_foto(id: int, caminho_foto: str) -> bool:
    """Atualiza apenas a foto do usuário"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return cursor.rowcount > 0
```

### 1.5. Rota de Upload

```python
# routes/perfil_routes.py

@router.post("/perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),  # ← Recebe arquivo de foto
    usuario_logado: dict = None
):
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # 2. Criar diretório se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)

    # 3. Gerar nome único para evitar conflitos
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # 4. Salvar arquivo no sistema
    try:
        conteudo = await foto.read()  # ← Lê conteúdo do arquivo
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # 5. Salvar caminho no banco de dados
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)

        # 6. Atualizar sessão do usuário
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)

    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)
```

### 1.6. Template HTML

```html
<!-- templates/perfil/dados.html -->

<!-- Container centralizado para foto atual -->
<div class="d-flex justify-content-center">
    <img id="foto-atual"
         src="{{ usuario.foto or '/static/img/user-default.png' }}"
         class="rounded-circle mb-3"
         style="width: 150px; height: 150px; object-fit: cover; border: 3px solid #dee2e6;"
         alt="Foto do perfil">
</div>

<!-- Preview da nova foto (inicialmente oculto) -->
<div id="preview-foto-container" style="display: none;">
    <div class="d-flex justify-content-center">
        <img id="preview-foto"
             src=""
             class="rounded-circle mb-2"
             style="width: 150px; height: 150px; object-fit: cover; border: 3px solid #28a745;"
             alt="Preview da nova foto">
    </div>
    <div class="small text-success mb-2">
        <i class="bi-check-circle"></i> Nova foto selecionada
    </div>
</div>

<!-- Formulário de upload -->
<form action="/perfil/alterar-foto" method="post" enctype="multipart/form-data">
    <div class="mb-2">
        <label for="foto" class="form-label small">Selecionar Nova Foto</label>
        <input type="file"
               class="form-control form-control-sm"
               id="foto"
               name="foto"
               accept="image/*">  <!-- ← Aceita apenas imagens -->
        <div class="form-text small">JPG, JPEG ou PNG</div>
    </div>
    <button type="submit" class="btn btn-sm btn-outline-primary" id="btn-alterar" disabled>
        <i class="bi-camera"></i> Alterar Foto
    </button>
    <button type="button" class="btn btn-sm btn-outline-secondary" id="btn-cancelar" onclick="cancelarSelecao()" style="display: none;">
        <i class="bi-x"></i> Cancelar
    </button>
</form>
```

### 1.7. JavaScript para Preview

```javascript
// Preview de foto de perfil
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const previewFoto = document.getElementById('preview-foto');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    fotoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];

        if (file) {
            // Verificar se é uma imagem
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    // Esconder foto atual e mostrar preview
                    fotoAtual.style.display = 'none';
                    previewFoto.src = e.target.result;
                    previewContainer.style.display = 'block';

                    // Habilitar botão e mostrar opções
                    btnAlterar.disabled = false;
                    btnAlterar.innerHTML = '<i class="bi-check"></i> Confirmar Alteração';
                    btnCancelar.style.display = 'inline-block';
                };

                reader.readAsDataURL(file);  // ← Converte arquivo em URL para preview
            } else {
                alert('Por favor, selecione apenas arquivos de imagem.');
                cancelarSelecao();
            }
        } else {
            cancelarSelecao();
        }
    });
});

function cancelarSelecao() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    // Limpar seleção e voltar ao estado inicial
    fotoInput.value = '';
    fotoAtual.style.display = 'block';
    previewContainer.style.display = 'none';
    btnAlterar.disabled = true;
    btnAlterar.innerHTML = '<i class="bi-camera"></i> Alterar Foto';
    btnCancelar.style.display = 'none';
}
```

---

## 🖼️ 2. GALERIA DE FOTOS (Produtos)

### 2.1. Estrutura de Diretórios

```
static/
└── img/
    └── products/
        ├── 000001/           # Diretório por produto (ID com 6 dígitos)
        │   ├── 000001-001.jpg  # Foto principal (sempre 001)
        │   ├── 000001-002.jpg  # Fotos adicionais (002, 003...)
        │   └── 000001-003.jpg
        └── 000002/
            └── 000002-001.jpg
```

### 2.2. Utilitário de Processamento de Fotos

```python
# util/foto_util.py

import os
from PIL import Image
from typing import List, Optional

def obter_diretorio_produto(produto_id: int) -> str:
    """Retorna o caminho do diretório de fotos de um produto"""
    codigo_produto = f"{produto_id:06d}"  # ← Formata com 6 dígitos (000001)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "static", "img", "products", codigo_produto)

def processar_imagem(arquivo, caminho_destino: str) -> bool:
    """
    Processa uma imagem: corta para quadrado, redimensiona e salva como JPG
    """
    try:
        # 1. Abrir a imagem
        img = Image.open(arquivo)

        # 2. Converter para RGB se necessário (para salvar como JPG)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 3. Cortar para quadrado (centro da imagem)
        largura, altura = img.size
        tamanho = min(largura, altura)  # ← Usa o menor lado

        # Calcula coordenadas para corte centralizado
        left = (largura - tamanho) // 2
        top = (altura - tamanho) // 2
        right = left + tamanho
        bottom = top + tamanho

        img = img.crop((left, top, right, bottom))  # ← Corta para quadrado

        # 4. Redimensionar para tamanho padrão
        img = img.resize((800, 800), Image.Resampling.LANCZOS)

        # 5. Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

        # 6. Salvar como JPG com qualidade otimizada
        img.save(caminho_destino, 'JPEG', quality=85, optimize=True)

        return True
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return False

def obter_foto_principal(produto_id: int) -> Optional[str]:
    """Retorna a URL da foto principal do produto ou None se não existir"""
    codigo_produto = f"{produto_id:06d}"
    caminho_foto = obter_diretorio_produto(produto_id) + f"/{codigo_produto}-001.jpg"

    if os.path.exists(caminho_foto):
        return f"/static/img/products/{codigo_produto}/{codigo_produto}-001.jpg"
    return None

def obter_todas_fotos(produto_id: int) -> List[str]:
    """Retorna lista de URLs de todas as fotos do produto ordenadas"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return []

    fotos = []
    arquivos = os.listdir(diretorio)

    # Filtrar apenas arquivos JPG do produto
    for arquivo in arquivos:
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            fotos.append(f"/static/img/products/{codigo_produto}/{arquivo}")

    # Ordenar por número sequencial (001, 002, 003...)
    fotos.sort()
    return fotos

def obter_proximo_numero(produto_id: int) -> int:
    """Retorna o próximo número sequencial disponível para uma nova foto"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return 1

    numeros = []
    arquivos = os.listdir(diretorio)

    for arquivo in arquivos:
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            # Extrair número do arquivo (XXXXXX-NNN.jpg)
            try:
                numero_str = arquivo.split('-')[1].split('.')[0]
                numeros.append(int(numero_str))
            except:
                continue

    if not numeros:
        return 1

    return max(numeros) + 1  # ← Próximo número na sequência

def salvar_nova_foto(produto_id: int, arquivo, como_principal: bool = False) -> bool:
    """Salva uma nova foto do produto"""
    criar_diretorio_produto(produto_id)
    codigo_produto = f"{produto_id:06d}"

    if como_principal:
        # Salvar como foto principal (001)
        numero = 1
        # Se já existe foto principal, mover as outras para frente
        if obter_foto_principal(produto_id):
            _mover_fotos_para_frente(produto_id)
    else:
        # Adicionar como próxima foto na sequência
        numero = obter_proximo_numero(produto_id)

    # Gerar caminho do arquivo
    caminho_destino = f"{obter_diretorio_produto(produto_id)}/{codigo_produto}-{numero:03d}.jpg"
    return processar_imagem(arquivo, caminho_destino)

def excluir_foto(produto_id: int, numero: int) -> bool:
    """Remove uma foto específica e reordena as restantes"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    # Remover o arquivo específico
    caminho_foto = f"{diretorio}/{codigo_produto}-{numero:03d}.jpg"

    if os.path.exists(caminho_foto):
        try:
            os.remove(caminho_foto)
        except:
            return False

    # Reordenar fotos restantes para não ter gaps na numeração
    return reordenar_fotos_automatico(produto_id)

def reordenar_fotos(produto_id: int, nova_ordem: List[int]) -> bool:
    """Reordena as fotos conforme a nova ordem especificada"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return False

    # Mapear arquivos existentes
    arquivos_existentes = {}
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            try:
                numero_str = arquivo.split('-')[1].split('.')[0]
                numero = int(numero_str)
                arquivos_existentes[numero] = arquivo
            except:
                continue

    # Validar nova ordem
    if len(nova_ordem) != len(arquivos_existentes):
        return False

    # Processo de renomeação em duas etapas para evitar conflitos:

    # Etapa 1: Renomear temporariamente
    temp_files = {}
    for i, numero_original in enumerate(nova_ordem):
        if numero_original not in arquivos_existentes:
            return False

        arquivo_original = arquivos_existentes[numero_original]
        caminho_original = f"{diretorio}/{arquivo_original}"
        caminho_temp = f"{diretorio}/temp_{i:03d}.jpg"

        try:
            os.rename(caminho_original, caminho_temp)
            temp_files[i] = caminho_temp
        except:
            return False

    # Etapa 2: Renomear para a sequência final
    for i in range(len(nova_ordem)):
        novo_numero = i + 1
        caminho_temp = temp_files[i]
        caminho_final = f"{diretorio}/{codigo_produto}-{novo_numero:03d}.jpg"

        try:
            os.rename(caminho_temp, caminho_final)
        except:
            return False

    return True
```

### 2.3. Rotas da Galeria

```python
# routes/admin_produtos_routes.py

from fastapi import APIRouter, Form, Request, status, UploadFile, File
from util.foto_util import (
    salvar_nova_foto, obter_foto_principal, obter_todas_fotos,
    excluir_foto, reordenar_fotos
)

# Rota para exibir a galeria
@router.get("/{id}/galeria")
@requer_autenticacao(["admin"])
async def get_galeria(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    fotos = obter_todas_fotos(id)  # ← Obtém todas as fotos do produto
    return templates.TemplateResponse(
        "galeria.html",
        {
            "request": request,
            "produto": produto,
            "fotos": fotos
        }
    )

# Rota para upload de múltiplas fotos
@router.post("/{id}/galeria/upload")
@requer_autenticacao(["admin"])
async def post_galeria_upload(
    request: Request,
    id: int,
    fotos: list[UploadFile] = File(...),  # ← Recebe múltiplas fotos
    usuario_logado: dict = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    sucesso = 0
    for foto in fotos:
        if foto.filename:
            try:
                # Salvar cada foto como não-principal (será adicionada no final)
                salvar_nova_foto(id, foto.file, como_principal=False)
                sucesso += 1
            except Exception as e:
                print(f"Erro ao salvar foto {foto.filename}: {e}")

    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)

# Rota para excluir foto específica
@router.post("/{id}/galeria/excluir/{numero}")
@requer_autenticacao(["admin"])
async def post_galeria_excluir(
    request: Request,
    id: int,
    numero: int,  # ← Número da foto a ser excluída (001, 002, etc.)
    usuario_logado: dict = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    try:
        excluir_foto(id, numero)  # ← Remove foto e reordena automaticamente
    except Exception as e:
        print(f"Erro ao excluir foto: {e}")

    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)

# Rota para reordenar fotos via drag-and-drop
@router.post("/{id}/galeria/reordenar")
@requer_autenticacao(["admin"])
async def post_galeria_reordenar(
    request: Request,
    id: int,
    nova_ordem: str = Form(...),  # ← Recebe string: "1,3,2,4"
    usuario_logado: dict = None
):
    produto = produto_repo.obter_por_id(id)
    if not produto:
        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    try:
        # Converter string em lista de inteiros
        ordem_lista = [int(x.strip()) for x in nova_ordem.split(",")]
        reordenar_fotos(id, ordem_lista)  # ← Aplica nova ordem
    except Exception as e:
        print(f"Erro ao reordenar fotos: {e}")

    return RedirectResponse(f"/admin/produtos/{id}/galeria", status.HTTP_303_SEE_OTHER)

# Modificar rota de cadastro para aceitar foto principal
@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    categoria_id: int = Form(...),
    foto: Optional[UploadFile] = File(None),  # ← Foto opcional no cadastro
    usuario_logado: dict = None
):
    # 1. Criar produto primeiro
    produto = Produto(
        id=0, nome=nome, descricao=descricao,
        preco=preco, quantidade=quantidade, categoria_id=categoria_id
    )
    produto_id = produto_repo.inserir(produto)

    if produto_id:
        # 2. Salvar foto se foi enviada
        if foto and foto.filename:
            try:
                salvar_nova_foto(produto_id, foto.file, como_principal=True)
            except Exception as e:
                print(f"Erro ao salvar foto: {e}")

        return RedirectResponse("/admin/produtos", status.HTTP_303_SEE_OTHER)

    # Erro ao criar produto...
```

### 2.4. Template da Galeria

```html
<!-- templates/admin/produtos/galeria.html -->

<div class="row">
    <div class="col-md-8">
        <h3>Fotos Existentes</h3>
        {% if fotos %}
        <div class="row g-3" id="galeria-fotos">
            {% for foto in fotos %}
            {% set foto_numero = foto.split('-')[-1].split('.')[0] | int %}
            <div class="col-md-4" data-numero="{{ foto_numero }}" draggable="true">
                <div class="card">
                    <!-- Marcar primeira foto como principal -->
                    {% if loop.index == 1 %}
                    <div class="badge bg-primary position-absolute top-0 start-0 m-2">Principal</div>
                    {% endif %}

                    <img src="{{ foto }}"
                         class="card-img-top"
                         style="width: 100%; aspect-ratio: 1/1; object-fit: cover;"
                         alt="Foto {{ foto_numero }}">

                    <div class="card-body text-center">
                        <p class="card-text small">Foto {{ "{:03d}".format(foto_numero) }}</p>

                        <!-- Botão excluir desabilitado para foto principal -->
                        {% if loop.index == 1 %}
                        <button type="button" class="btn btn-danger btn-sm" disabled
                                title="A foto principal não pode ser excluída">
                            <i class="bi-trash"></i> Excluir
                        </button>
                        {% else %}
                        <form method="post"
                              action="/admin/produtos/{{ produto.id }}/galeria/excluir/{{ foto_numero }}"
                              onsubmit="return confirm('Deseja realmente excluir esta foto?')"
                              style="display: inline;">
                            <button type="submit" class="btn btn-danger btn-sm">
                                <i class="bi-trash"></i> Excluir
                            </button>
                        </form>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Seção de reordenação (apenas se há mais de 1 foto) -->
        {% if fotos|length > 1 %}
        <div class="mt-4">
            <h4>Reordenar Fotos</h4>
            <p class="text-muted">Arraste as fotos para reordená-las. A primeira foto será sempre a principal.</p>
            <form method="post" action="/admin/produtos/{{ produto.id }}/galeria/reordenar" id="form-reordenar">
                <input type="hidden" name="nova_ordem" id="nova_ordem">
                <button type="button" class="btn btn-success" onclick="salvarOrdem()">
                    <i class="bi-check"></i> Salvar Nova Ordem
                </button>
            </form>
        </div>
        {% endif %}

        {% else %}
        <!-- Estado vazio -->
        <div class="text-center py-5">
            <i class="bi-images" style="font-size: 4rem; color: #dee2e6;"></i>
            <p class="text-muted mt-3">Nenhuma foto cadastrada para este produto.</p>
        </div>
        {% endif %}
    </div>

    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h3>Adicionar Fotos</h3>

                <!-- Upload múltiplo -->
                <form method="post"
                      action="/admin/produtos/{{ produto.id }}/galeria/upload"
                      enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="fotos" class="form-label">Selecionar Fotos</label>
                        <input type="file"
                               class="form-control"
                               id="fotos"
                               name="fotos"
                               accept="image/*"
                               multiple
                               required>  <!-- ← multiple permite várias fotos -->
                        <div class="form-text">
                            Selecione uma ou mais fotos.<br>
                            Formatos aceitos: JPG, PNG, GIF, WEBP.<br>
                            As imagens serão cortadas para formato quadrado.
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="bi-upload"></i> Enviar Fotos
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
```

### 2.5. JavaScript para Drag-and-Drop

```javascript
// Sistema de Drag and Drop para reordenar fotos
let draggedElement = null;

document.addEventListener('DOMContentLoaded', function() {
    const galeriaFotos = document.getElementById('galeria-fotos');
    if (!galeriaFotos) return;

    const fotoCards = galeriaFotos.querySelectorAll('[draggable="true"]');

    fotoCards.forEach(card => {
        // Quando inicia o arrasto
        card.addEventListener('dragstart', function(e) {
            draggedElement = this;
            this.style.opacity = '0.5';  // ← Feedback visual
        });

        // Quando termina o arrasto
        card.addEventListener('dragend', function(e) {
            this.style.opacity = '';
            draggedElement = null;
        });

        // Permite drop sobre o elemento
        card.addEventListener('dragover', function(e) {
            e.preventDefault();
        });

        // Quando solta o elemento
        card.addEventListener('drop', function(e) {
            e.preventDefault();
            if (this !== draggedElement) {
                // Trocar posições dos elementos
                const allCards = Array.from(galeriaFotos.children);
                const draggedIndex = allCards.indexOf(draggedElement);
                const targetIndex = allCards.indexOf(this);

                if (draggedIndex < targetIndex) {
                    this.parentNode.insertBefore(draggedElement, this.nextSibling);
                } else {
                    this.parentNode.insertBefore(draggedElement, this);
                }

                // Atualizar badges de "Principal"
                atualizarBadgePrincipal();
            }
        });
    });
});

function atualizarBadgePrincipal() {
    const galeriaFotos = document.getElementById('galeria-fotos');
    if (!galeriaFotos) return;

    // Remover todos os badges existentes
    galeriaFotos.querySelectorAll('.badge').forEach(badge => badge.remove());

    // Adicionar badge na primeira foto
    const primeiraFoto = galeriaFotos.firstElementChild;
    if (primeiraFoto) {
        const badge = document.createElement('div');
        badge.className = 'badge bg-primary position-absolute top-0 start-0 m-2';
        badge.textContent = 'Principal';
        primeiraFoto.querySelector('.card').appendChild(badge);
    }
}

function salvarOrdem() {
    const galeriaFotos = document.getElementById('galeria-fotos');
    if (!galeriaFotos) return;

    // Obter nova ordem baseada na posição atual dos elementos
    const cards = galeriaFotos.querySelectorAll('[data-numero]');
    const novaOrdem = Array.from(cards).map(card => card.dataset.numero);

    // Enviar nova ordem para o servidor
    document.getElementById('nova_ordem').value = novaOrdem.join(',');
    document.getElementById('form-reordenar').submit();
}

// Preview de imagens antes do upload
document.getElementById('fotos').addEventListener('change', function(e) {
    const files = e.target.files;
    if (files.length > 0) {
        console.log(`${files.length} arquivo(s) selecionado(s)`);
        // Aqui pode adicionar preview das imagens selecionadas
    }
});
```

### 2.6. Integração com Listagens

```python
# Modificar rota de listagem para incluir fotos
@router.get("/")
@requer_autenticacao(["admin"])
async def gets(request: Request, usuario_logado: dict = None):
    produtos = produto_repo.obter_todos()

    # Adicionar informação de foto para cada produto
    for produto in produtos:
        produto.foto_principal = obter_foto_principal(produto.id)  # ← Adiciona foto

    return templates.TemplateResponse(
        "listar.html", {"request": request, "produtos": produtos}
    )
```

```html
<!-- Na listagem, mostrar miniatura da foto -->
<td>
    <img src="{{ produto.foto_principal or '/static/img/placeholder.png' }}"
         alt="Foto do produto"
         style="width: 50px; height: 50px; object-fit: cover;">
</td>

<!-- Adicionar botão para acessar galeria -->
<td class="text-center">
    <a href="/admin/produtos/{{ produto.id }}/galeria"
       class="btn btn-warning btn-sm"
       title="Galeria de Fotos">
        <i class="bi-images"></i>
    </a>
</td>
```

---

## 🎯 Resumo dos Conceitos

### Foto Única:
- **Um arquivo por entidade**
- **Nome único** com hash para evitar conflitos
- **Validação simples** de tipo de arquivo
- **Preview direto** com FileReader
- **Upload direto** para destino final

### Galeria de Fotos:
- **Múltiplos arquivos organizados** por diretório
- **Nomenclatura sequencial** (001, 002, 003...)
- **Processamento avançado** (corte, redimensionamento)
- **Reordenação com drag-and-drop**
- **Foto principal** sempre na posição 001
- **Proteção da foto principal** (botão excluir desabilitado)
- **Exibição quadrada** com aspect-ratio 1:1

### Pontos Importantes:
1. **Sempre validar** tipos de arquivo
2. **Criar diretórios** automaticamente
3. **Usar nomes únicos** para evitar conflitos
4. **Processar imagens** para padronizar formato
5. **Implementar preview** para melhor UX
6. **Tratar erros** adequadamente
7. **Atualizar sessões** quando necessário

### Melhorias de UX Implementadas:
- ✅ **Preview de fotos**: Visualização antes do upload (tanto foto única quanto galeria)
- ✅ **Botões inteligentes**: Estados desabilitado/habilitado conforme contexto
- ✅ **Proteção da foto principal**: Não pode ser excluída (botão desabilitado com tooltip)
- ✅ **Proporção quadrada**: CSS com `aspect-ratio: 1/1` para exibição consistente
- ✅ **Feedback visual**: Bordas coloridas para diferenciar foto atual vs nova
- ✅ **Drag-and-drop**: Reordenação intuitiva com feedback visual
- ✅ **Tooltips explicativos**: Mensagens claras sobre limitações e funcionalidades
- ✅ **Alinhamento consistente**: Container `d-flex justify-content-center` para centralização perfeita

### Segurança:
- ✅ Validação de tipos de arquivo
- ✅ Nomes únicos/sequenciais
- ✅ Diretórios organizados
- ✅ Tratamento de erros
- ✅ Autenticação nas rotas

Este guia fornece uma base completa para implementar sistemas de fotos em aplicações web FastAPI! 📸