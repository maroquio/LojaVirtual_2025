import os
from PIL import Image
from typing import List, Optional


def obter_diretorio_produto(produto_id: int) -> str:
    """Retorna o caminho do diretório de fotos de um produto"""
    codigo_produto = f"{produto_id:06d}"
    # Usar caminho relativo ao diretório atual
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "static", "img", "products", codigo_produto)


def obter_url_diretorio_produto(produto_id: int) -> str:
    """Retorna a URL do diretório de fotos de um produto"""
    codigo_produto = f"{produto_id:06d}"
    return f"/static/img/products/{codigo_produto}"


def criar_diretorio_produto(produto_id: int) -> bool:
    """Cria o diretório de fotos do produto se não existir"""
    try:
        diretorio = obter_diretorio_produto(produto_id)
        os.makedirs(diretorio, exist_ok=True)
        return True
    except:
        return False


def processar_imagem(arquivo, caminho_destino: str) -> bool:
    """
    Processa uma imagem: corta para quadrado, redimensiona e salva como JPG
    """
    try:
        # Abrir a imagem
        img = Image.open(arquivo)

        # Converter para RGB se necessário (para salvar como JPG)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Cortar para quadrado (centro da imagem)
        largura, altura = img.size
        tamanho = min(largura, altura)

        left = (largura - tamanho) // 2
        top = (altura - tamanho) // 2
        right = left + tamanho
        bottom = top + tamanho

        img = img.crop((left, top, right, bottom))

        # Redimensionar para tamanho padrão
        img = img.resize((800, 800), Image.Resampling.LANCZOS)

        # Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

        # Salvar como JPG
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

    # Ordenar por número sequencial
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

    return max(numeros) + 1


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

    # Reordenar fotos restantes
    return reordenar_fotos_automatico(produto_id)


def reordenar_fotos_automatico(produto_id: int) -> bool:
    """Reordena automaticamente as fotos para não ter gaps na numeração"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    if not os.path.exists(diretorio):
        return True

    # Obter todas as fotos ordenadas
    arquivos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            arquivos.append(arquivo)

    arquivos.sort()

    # Renomear temporariamente para evitar conflitos
    temp_files = []
    for i, arquivo in enumerate(arquivos):
        caminho_original = f"{diretorio}/{arquivo}"
        caminho_temp = f"{diretorio}/temp_{i:03d}.jpg"
        try:
            os.rename(caminho_original, caminho_temp)
            temp_files.append(caminho_temp)
        except:
            return False

    # Renomear para a sequência final
    for i, caminho_temp in enumerate(temp_files):
        novo_numero = i + 1
        caminho_final = f"{diretorio}/{codigo_produto}-{novo_numero:03d}.jpg"
        try:
            os.rename(caminho_temp, caminho_final)
        except:
            return False

    return True


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

    # Renomear temporariamente
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

    # Renomear para a sequência final
    for i in range(len(nova_ordem)):
        novo_numero = i + 1
        caminho_temp = temp_files[i]
        caminho_final = f"{diretorio}/{codigo_produto}-{novo_numero:03d}.jpg"

        try:
            os.rename(caminho_temp, caminho_final)
        except:
            return False

    return True


def salvar_nova_foto(produto_id: int, arquivo, como_principal: bool = False) -> bool:
    """Salva uma nova foto do produto"""
    criar_diretorio_produto(produto_id)
    codigo_produto = f"{produto_id:06d}"

    if como_principal:
        # Salvar como foto principal (001)
        numero = 1
        # Se já existe foto principal, mover as outras
        if obter_foto_principal(produto_id):
            _mover_fotos_para_frente(produto_id)
    else:
        # Adicionar como próxima foto
        numero = obter_proximo_numero(produto_id)

    caminho_destino = f"{obter_diretorio_produto(produto_id)}/{codigo_produto}-{numero:03d}.jpg"
    return processar_imagem(arquivo, caminho_destino)


def _mover_fotos_para_frente(produto_id: int):
    """Move todas as fotos existentes uma posição para frente"""
    codigo_produto = f"{produto_id:06d}"
    diretorio = obter_diretorio_produto(produto_id)

    arquivos = []
    for arquivo in os.listdir(diretorio):
        if arquivo.startswith(codigo_produto) and arquivo.endswith('.jpg'):
            arquivos.append(arquivo)

    # Ordenar em ordem reversa para não sobrescrever
    arquivos.sort(reverse=True)

    for arquivo in arquivos:
        try:
            numero_str = arquivo.split('-')[1].split('.')[0]
            numero_atual = int(numero_str)
            novo_numero = numero_atual + 1

            caminho_atual = f"{diretorio}/{arquivo}"
            novo_arquivo = f"{codigo_produto}-{novo_numero:03d}.jpg"
            caminho_novo = f"{diretorio}/{novo_arquivo}"

            os.rename(caminho_atual, caminho_novo)
        except:
            continue