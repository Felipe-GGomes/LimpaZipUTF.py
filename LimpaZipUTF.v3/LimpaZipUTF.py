"""
Script para EXTRAIR e ORGANIZAR arquivos de disciplinas da UTFPR
Move arquivos úteis para a raiz, remove apenas lixo
Funcionalidades:
  - Extrai e organiza arquivos
  - Descompacta .zip, .rar, .7z em pasta ZIPS
  - Organiza arquivos por extensão em pastas
Autor: Felipe Gabriel Gomes
Nome obrigatório: LimpaZipUTF
"""

import os
import shutil
from pathlib import Path
from typing import Set, Dict, List
import zipfile
import subprocess
import sys


# Extensões de arquivos que Vamos MANTER e EXTRAIR
EXTENSOES_PERMITIDAS: Set[str] = {
    # Documentos
    '.pdf',
    '.doc', '.docx',
    '.ppt', '.pptx',
    '.xls', '.xlsx',

    # Código
    '.java',
    '.py',
    '.c', '.cpp', '.h', '.hpp',
    '.js', '.html', '.css',
    '.sql',
    '.class',
    '.jar',

    # Texto
    '.txt',
    '.md',
    '.csv',

    # Imagens
    '.png', '.jpg', '.jpeg',
    '.gif', '.svg',

    # Compactados
    '.zip', '.rar', '.7z',
    
    #voce pode adicionar outras extensoes aqui se quiser!
}

# Mapeamento de extensões para pastas
#se você quiser adicionar outras categorias, faça aqui!
CATEGORIAS_EXTENSOES: Dict[str, Set[str]] = {
    'Documentos': {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'},
    'Código': {'.java', '.py', '.c', '.cpp', '.h', '.hpp', '.js', '.html', '.css', '.sql', '.class', '.jar'},
    'Texto': {'.txt', '.md', '.csv'},
    'Imagens': {'.png', '.jpg', '.jpeg', '.gif', '.svg'},
    'Compactados': {'.zip', '.rar', '.7z'},
}

# Arquivos a REMOVER
# se quiser adicionar outros arquivos para remover, faça aqui!
ARQUIVOS_PARA_REMOVER: Set[str] = {
    'index.html',
    'index.htm',
    'index.php',
    'thumbs.db',
    '.ds_store',
    'desktop.ini',
    'comet_html_doc.xml',
}

# Arquivo do organizador (não deve ser movido para Código)
ARQUIVO_ORGANIZADOR = 'LimpaZipUTF.py'

# Pasta especial para descompactados
# você pode mudar o nome se quiser
PASTA_ZIPS = 'ZIPS'

# Verifica se um arquivo deve ser mantido
def deve_manter_arquivo(caminho: Path) -> bool:
    if caminho.name.lower() in ARQUIVOS_PARA_REMOVER:
        return False

    extensao = caminho.suffix.lower()
    return extensao in EXTENSOES_PERMITIDAS

#EXTRAI arquivos úteis de subpastas para a raiz da pasta.
#Remove apenas arquivos completamente inúteis.
def extrair_e_organizar(pasta_raiz: str, modo_simulacao: bool = True, verbose: bool = True) -> dict:
    """
    Args:
        pasta_raiz: Caminho da pasta raiz
        modo_simulacao: Se True, apenas mostra o que seria movido
        verbose: Se True, mostra detalhes
    Returns:
        Dicionário com estatísticas
    """
    pasta_raiz = Path(pasta_raiz)

    if not pasta_raiz.exists():
        raise ValueError(f"Pasta não encontrada: {pasta_raiz}")

    estatisticas = {
        'arquivos_movidos': 0,
        'arquivos_removidos': 0,
        'pastas_vazias_removidas': 0,
        'arquivos_movidos_lista': [],
        'arquivos_removidos_lista': [],
        'espaco_liberado_mb': 0,
        'arquivos_compactados_encontrados': [],
    }

    print(f"\n{'[SIMULAÇÃO]' if modo_simulacao else '[EXECUÇÃO]'} Processando: {pasta_raiz}")
    print("-" * 120)

    '''
    =============================================================================
                    DE PREFERENCIA NÃO ALTERE O CÓDIGO ABAIXO
    =============================================================================
    '''

    # 1️⃣ PRIMEIRO PASSO: Procura arquivos úteis em subpastas e MOVE para a raiz
    for item in pasta_raiz.rglob('*'):
        try:
            # Só processa arquivos (não pastas)
            if item.is_file():
                # Não mover arquivos que já estão na raiz
                if item.parent == pasta_raiz:
                    if deve_manter_arquivo(item):
                        if item.suffix.lower() in {'.zip', '.rar', '.7z'}:
                            estatisticas['arquivos_compactados_encontrados'].append(item.name)
                    continue

                # Verificar se é um arquivo útil
                if deve_manter_arquivo(item):
                    # Arquivos úteis: MOVER para a raiz
                    novo_caminho = pasta_raiz / item.name

                    # Se já existe na raiz, adiciona sufixo
                    if novo_caminho.exists():
                        novo_caminho = pasta_raiz / f"{item.stem}_copia{item.suffix}"

                    if verbose:
                        print(f"📤 MOVENDO: {item.relative_to(pasta_raiz)} → {novo_caminho.name}")

                    estatisticas['arquivos_movidos'] += 1
                    estatisticas['arquivos_movidos_lista'].append(f"{item.relative_to(pasta_raiz)} → {novo_caminho.name}")

                    if not modo_simulacao:
                        shutil.move(str(item), str(novo_caminho))

                    # Registra arquivos compactados encontrados
                    if item.suffix.lower() in {'.zip', '.rar', '.7z'}:
                        estatisticas['arquivos_compactados_encontrados'].append(novo_caminho.name)

                else:
                    # Arquivos inúteis: REMOVER
                    tamanho_mb = item.stat().st_size / (1024 * 1024)
                    estatisticas['espaco_liberado_mb'] += tamanho_mb
                    estatisticas['arquivos_removidos'] += 1
                    estatisticas['arquivos_removidos_lista'].append(str(item.relative_to(pasta_raiz)))

                    if verbose:
                        print(f"🗑️  REMOVENDO: {item.relative_to(pasta_raiz)} ({tamanho_mb:.2f} MB)")

                    if not modo_simulacao:
                        item.unlink()

        except Exception as e:
            print(f"⚠️  Erro ao processar {item}: {e}")

    # 2️⃣ SEGUNDO PASSO: Remove pastas vazias
    if not modo_simulacao:
        for pasta in sorted(pasta_raiz.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if pasta.is_dir():
                try:
                    # Verifica se está vazia
                    if not any(pasta.iterdir()):
                        pasta.rmdir()
                        estatisticas['pastas_vazias_removidas'] += 1
                        if verbose:
                            print(f"📁 PASTA VAZIA REMOVIDA: {pasta.relative_to(pasta_raiz)}")
                except:
                    pass

    return estatisticas

#Descompacta um arquivo (ZIP, RAR ou 7Z).
#Tenta diferentes métodos dependendo do tipo.
def descompactar_arquivo(caminho_arquivo: Path, pasta_destino: Path, verbose: bool = True) -> bool:
    
    """
    Args:
        caminho_arquivo: Caminho do arquivo a descompactar
        pasta_destino: Pasta de destino
        verbose: Se True, mostra detalhes
        
    Returns:
        True se sucesso, False se erro
    """
    
    extensao = caminho_arquivo.suffix.lower()
    
    try:
        if extensao == '.zip':
            # Descompacta ZIP usando zipfile nativo
            try:
                with zipfile.ZipFile(str(caminho_arquivo), 'r') as zip_ref:
                    zip_ref.extractall(str(pasta_destino))
                if verbose:
                    print(f"✅ ZIP descompactado com sucesso!")
                return True
            except zipfile.BadZipFile:
                print(f"❌ Arquivo .zip inválido ou corrompido")
                return False
                
        elif extensao in {'.rar', '.7z'}:
            # Tenta usar 7-Zip se disponível (melhor suporte para RAR)
            try:
                # Tenta localizar 7z ou WinRAR
                programas = [
                    'C:\\Program Files\\7-Zip\\7z.exe',
                    'C:\\Program Files (x86)\\7-Zip\\7z.exe',
                    'C:\\Program Files\\WinRAR\\UnRAR.exe',
                    'C:\\Program Files (x86)\\WinRAR\\UnRAR.exe',
                    '7z',
                    'unrar',
                ]
                
                executado = False
                for programa in programas:
                    try:
                        if extensao == '.rar':
                            # Tenta com UnRAR
                            if 'unrar' in programa.lower() or 'winrar' in programa.lower():
                                subprocess.run(
                                    [programa, 'x', str(caminho_arquivo), str(pasta_destino)],
                                    check=True,
                                    capture_output=True,
                                    timeout=60
                                )
                                executado = True
                                if verbose:
                                    print(f"✅ RAR descompactado com sucesso!")
                                break
                            # Tenta com 7z
                            else:
                                subprocess.run(
                                    [programa, 'x', str(caminho_arquivo), f'-o{str(pasta_destino)}'],
                                    check=True,
                                    capture_output=True,
                                    timeout=60
                                )
                                executado = True
                                if verbose:
                                    print(f"✅ RAR descompactado com sucesso!")
                                break
                        else:  # .7z
                            subprocess.run(
                                [programa, 'x', str(caminho_arquivo), f'-o{str(pasta_destino)}'],
                                check=True,
                                capture_output=True,
                                timeout=60
                            )
                            executado = True
                            if verbose:
                                print(f"✅ 7Z descompactado com sucesso!")
                            break
                    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                        continue
                
                if executado:
                    return True
                else:
                    print(f"⚠️  Nenhum descompactador disponível para {extensao}")
                    print(f"    Instale: 7-Zip ou WinRAR para descompactar {extensao}")
                    return False
                    
            except Exception as e:
                print(f"❌ Erro ao descompactar {extensao}: {e}")
                return False
        else:
            print(f"❌ Formato não suportado: {extensao}")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

#Descompacta todos os arquivos .zip, .rar, .7z encontrados.
#Cria uma pasta ZIPS com o arquivo compactado e pasta_quak para descompactado
def descompactar_compactados(pasta_raiz: str, arquivos_compactados: List[str], verbose: bool = True) -> dict:
    
    """
    Args:
        pasta_raiz: Caminho da pasta raiz
        arquivos_compactados: Lista de arquivos compactados para descompactar
        verbose: Se True, mostra detalhes

    Returns:
        Dicionário com estatísticas
    """
    
    pasta_raiz = Path(pasta_raiz)
    pasta_zips_path = pasta_raiz / PASTA_ZIPS
    
    estatisticas = {
        'arquivos_descompactados': 0,
        'erros': [],
        'compactados_movidos': 0,
    }

    if not arquivos_compactados:
        print("\n✅ Nenhum arquivo compactado encontrado!")
        return estatisticas

    # Cria pasta ZIPS se não existir
    if not pasta_zips_path.exists():
        pasta_zips_path.mkdir(exist_ok=True, parents=True)
        print(f"📁 Pasta criada: {PASTA_ZIPS}/")

    print(f"\n{'=' * 120}")
    print(f"📦 DESCOMPACTANDO {len(arquivos_compactados)} ARQUIVO(S) COMPACTADO(S)")
    print(f"{'=' * 120}")

    for nome_arquivo in arquivos_compactados:
        caminho_arquivo = pasta_raiz / nome_arquivo
        
        if not caminho_arquivo.exists():
            print(f"\n⚠️  Arquivo não encontrado: {nome_arquivo}")
            continue

        try:
            # Cria pasta com nome do arquivo + "quak" DENTRO de ZIPS
            # voce pode mudar o sufixo se quiser
            nome_base = Path(nome_arquivo).stem  # Nome sem extensão
            nome_pasta = f"{nome_base}_quak" #<-- você pode mudar o sufixo aqui se quiser
            pasta_destino = pasta_zips_path / nome_pasta
            
            print(f"\n📦 Descompactando: {nome_arquivo}")
            print(f"📁 Criando pasta: {PASTA_ZIPS}/{nome_pasta}/")
            
            # Cria a pasta de destino se não existir
            pasta_destino.mkdir(exist_ok=True, parents=True)
            
            # Tenta descompactar
            sucesso = descompactar_arquivo(caminho_arquivo, pasta_destino, verbose)
            
            if sucesso:
                estatisticas['arquivos_descompactados'] += 1
                print(f"✅ Descompactado com sucesso em: {PASTA_ZIPS}/{nome_pasta}/")
                
                # Move o arquivo compactado para pasta ZIPS
                try:
                    caminho_novo_zip = pasta_zips_path / nome_arquivo
                    shutil.move(str(caminho_arquivo), str(caminho_novo_zip))
                    estatisticas['compactados_movidos'] += 1
                    print(f"📦 Arquivo compactado movido para: {PASTA_ZIPS}/{nome_arquivo}")
                except Exception as e:
                    print(f"⚠️  Erro ao mover {nome_arquivo}: {e}")
            else:
                estatisticas['erros'].append(f"{nome_arquivo}: Falha na descompactação")
                # Remove pasta vazia se falhou
                try:
                    if pasta_destino.exists() and not any(pasta_destino.iterdir()):
                        pasta_destino.rmdir()
                except:
                    pass

        except Exception as e:
            print(f"❌ Erro geral ao processar {nome_arquivo}: {e}")
            estatisticas['erros'].append(f"{nome_arquivo}: {str(e)}")

    return estatisticas

#Organiza os arquivos em pastas de acordo com a extensão.
#NÃO move compactados (.zip, .rar, .7z) e não move LimpaZipUTF.py
def organizar_por_extensao(pasta_raiz: str, modo_simulacao: bool = True, verbose: bool = True) -> dict:
    
    """
    Args:
        pasta_raiz: Caminho da pasta raiz
        modo_simulacao: Se True, apenas mostra o que seria movido
        verbose: Se True, mostra detalhes

    Returns:
        Dicionário com estatísticas
    """
    
    pasta_raiz = Path(pasta_raiz)

    if not pasta_raiz.exists():
        raise ValueError(f"Pasta não encontrada: {pasta_raiz}")

    estatisticas = {
        'arquivos_movidos': 0,
        'pastas_criadas': 0,
        'movimentos': [],
    }

    print(f"\n{'[SIMULAÇÃO]' if modo_simulacao else '[EXECUÇÃO]'} Organizando por extensão: {pasta_raiz}")
    print("-" * 120)

    # Contar arquivos por categoria
    contagem_por_categoria = {cat: 0 for cat in CATEGORIAS_EXTENSOES.keys()}
    
    for arquivo in pasta_raiz.glob('*'):
        if arquivo.is_file():
            # Pula o arquivo do organizador
            if arquivo.name == ARQUIVO_ORGANIZADOR:
                continue
            
            # Pula arquivos compactados (eles foram movidos para ZIPS)
            if arquivo.suffix.lower() in {'.zip', '.rar', '.7z'}:
                continue
                
            extensao = arquivo.suffix.lower()
            for categoria, extensoes in CATEGORIAS_EXTENSOES.items():
                if extensao in extensoes:
                    contagem_por_categoria[categoria] += 1
                    break

    # Mostrar preview
    print("\n📊 PREVIEW - Arquivos por categoria:")
    print("-" * 120)
    for categoria, quantidade in contagem_por_categoria.items():
        if quantidade > 0:
            print(f"  📁 {categoria}: {quantidade} arquivo(s)")

    # Processar movimentos
    for arquivo in pasta_raiz.glob('*'):
        if arquivo.is_file() and arquivo.suffix.lower() in EXTENSOES_PERMITIDAS:
            # Pula o arquivo do organizador
            if arquivo.name == ARQUIVO_ORGANIZADOR:
                if verbose:
                    print(f"⏭️  IGNORANDO: {arquivo.name} (arquivo do organizador)")
                continue
            
            # Pula arquivos compactados
            if arquivo.suffix.lower() in {'.zip', '.rar', '.7z'}:
                if verbose:
                    print(f"⏭️  IGNORANDO: {arquivo.name} (arquivo compactado - será movido para ZIPS)")
                continue
                
            extensao = arquivo.suffix.lower()
            
            # Encontra a categoria
            categoria = None
            for cat, extensoes in CATEGORIAS_EXTENSOES.items():
                if extensao in extensoes:
                    categoria = cat
                    break

            if categoria:
                # Cria pasta se não existir
                pasta_categoria = pasta_raiz / categoria
                
                if not modo_simulacao:
                    pasta_categoria.mkdir(exist_ok=True)
                    if not pasta_categoria.exists():
                        estatisticas['pastas_criadas'] += 1

                novo_caminho = pasta_categoria / arquivo.name

                if verbose:
                    print(f"📂 MOVENDO: {arquivo.name} → {categoria}/")

                estatisticas['arquivos_movidos'] += 1
                estatisticas['movimentos'].append(f"{arquivo.name} → {categoria}/")

                if not modo_simulacao:
                    shutil.move(str(arquivo), str(novo_caminho))

    return estatisticas


def imprimir_estatisticas(stats: dict, modo_simulacao: bool = True):
    """Imprime as estatísticas."""
    print("\n" + "=" * 120)
    print("📊 ESTATÍSTICAS DA OPERAÇÃO")
    print("=" * 120)
    print(f"Arquivos MOVIDOS para raiz: {stats['arquivos_movidos']}")
    print(f"Arquivos REMOVIDOS (lixo): {stats['arquivos_removidos']}")
    print(f"Pastas vazias removidas: {stats['pastas_vazias_removidas']}")
    print(f"Espaço liberado: {stats['espaco_liberado_mb']:.2f} MB")
    
    if stats['arquivos_compactados_encontrados']:
        print(f"Arquivos compactados encontrados: {len(stats['arquivos_compactados_encontrados'])}")
    
    print("=" * 120)

    if modo_simulacao:
        print("\n💡 Para executar, rode novamente com --executar")
    else:
        print("\n✅ Organização concluída!")


def imprimir_extensoes():
    """Imprime as extensões organizadas por categoria."""
    print("\n" + "=" * 120)
    print("📋 EXTENSÕES PERMITIDAS")
    print("=" * 120)
    for categoria, extensoes in CATEGORIAS_EXTENSOES.items():
        print(f"\n{categoria}:")
        print(f"  {', '.join(sorted(extensoes))}")
    print("\n" + "=" * 120)


def main():
    """Função principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description='EXTRAI, DESCOMPACTA e ORGANIZA arquivos úteis de disciplinas da UTFPR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python LimpaZipUTF.py /caminho/da/pasta
  python LimpaZipUTF.py /caminho/da/pasta --executar
  python LimpaZipUTF.py /caminho/da/pasta --executar --silencioso
  python LimpaZipUTF.py /caminho/da/pasta --extensoes
        """
    )
    # a cima são as opções do parser (comandos de terminal)

    # !!!NÃO ALTERE O CÓDIGO ABAIXO!!!
    parser.add_argument('pasta', help='Caminho da pasta a organizar')
    parser.add_argument('--executar', action='store_true', help='Executa a extração (padrão: simulação)')
    parser.add_argument('--silencioso', action='store_true', help='Modo menos verboso')
    parser.add_argument('--extensoes', action='store_true', help='Mostra extensões permitidas e sai')

    args = parser.parse_args()

    if args.extensoes:
        imprimir_extensoes()
        return 0

    modo_simulacao = not args.executar
    verbose = not args.silencioso

    if modo_simulacao:
        print("\n⚠️  MODO SIMULAÇÃO - Nenhum arquivo será movido ou removido")
        print("💡 Use --executar para realmente fazer a extração\n")
    else:
        print("\n⚠️  MODO EXECUÇÃO - ARQUIVOS SERÃO MOVIDOS E PASTAS REMOVIDAS!")
        resposta = input("Tem certeza? Digite 'y' para continuar: ").strip().lower()
        if resposta != 'y':
            print("Operação cancelada.")
            return 0
        print()

    try:
        # 1️⃣ PASSO 1: Extrair e organizar
        stats = extrair_e_organizar(args.pasta, modo_simulacao, verbose)
        imprimir_estatisticas(stats, modo_simulacao)

        # 2️⃣ PASSO 2: Descompactar arquivos compactados (ANTES de organizar!)
        if not modo_simulacao:
            if stats['arquivos_compactados_encontrados']:
                print(f"\n📦 Encontrados {len(stats['arquivos_compactados_encontrados'])} arquivo(s) compactado(s):")
                for arquivo in stats['arquivos_compactados_encontrados']:
                    print(f"  • {arquivo}")
                
                resposta_descomp = input("\n[y/n] Descompactar todos? ").strip().lower()
                
                if resposta_descomp == 'y':
                    stats_descomp = descompactar_compactados(args.pasta, stats['arquivos_compactados_encontrados'], verbose)
                    print(f"\n✅ Descompactados: {stats_descomp['arquivos_descompactados']}")
                    print(f"📦 Compactados movidos para ZIPS: {stats_descomp['compactados_movidos']}")
                    
                    if stats_descomp['erros']:
                        print(f"\n⚠️  Erros encontrados:")
                        for erro in stats_descomp['erros']:
                            print(f"  • {erro}")

        # 3️⃣ PASSO 3: Organizar por extensão (DEPOIS de descompactar)
        if not modo_simulacao:
            resposta_org = input("\n[y/n] Organizar arquivos por extensão (Documentos, Código, Imagens, etc)? ").strip().lower()
            
            if resposta_org == 'y':
                stats_org = organizar_por_extensao(args.pasta, False, verbose)
                print(f"\n✅ Arquivos organizados: {stats_org['arquivos_movidos']}")
                print(f"📁 Pastas criadas: {stats_org['pastas_criadas']}")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())

# só 600 linhas de código! ufa!