"""
Script de Engenharia de Dados: Extração de XML para DataFrame Pandas
=====================================================================

Autor: Desenvolvedor Python Especialista em Engenharia de Dados
Objetivo: Extrair dados de tags específicas de um XML e transformá-los em DataFrame

Dependências:
- xml.etree.ElementTree: Para parsing do XML
- pandas: Para estruturação dos dados em DataFrame
"""

import xml.etree.ElementTree as ET
import pandas as pd
from typing import List, Dict, Any


def extrair_texto_limpo(elemento: ET.Element) -> str:
    """
    Extrai o texto limpo de um elemento XML, incluindo texto de sub-elementos.
    
    Esta função utiliza itertext() para capturar todo o conteúdo textual,
    ignorando as tags XML internas e retornando apenas o valor bruto.
    
    Args:
        elemento: Elemento XML do qual extrair o texto
        
    Returns:
        String com o texto limpo (vazio se não houver texto)
    """
    # itertext() percorre recursivamente todos os nós de texto
    # ''.join() concatena todos os textos encontrados
    # strip() remove espaços em branco nas extremidades
    texto = ''.join(elemento.itertext()).strip()
    return texto if texto else ''


def xml_para_dataframe(
    caminho_xml: str,
    tag_pai: str,
    *tags_filhas: str
) -> pd.DataFrame:
    """
    Extrai dados de um arquivo XML e retorna um DataFrame Pandas.
    
    O script navega pelo XML localizando todas as ocorrências da tag_pai,
    e para cada ocorrência, extrai os valores das tags_filhas especificadas.
    
    Args:
        caminho_xml: Caminho completo do arquivo XML
        tag_pai: Nome da tag de segunda ordem que agrupa os dados (ex: 'titprivado')
        *tags_filhas: Nomes das tags cujos valores serão extraídos (aceita múltiplas tags)
        
    Returns:
        DataFrame Pandas com colunas nomeadas conforme as tags_filhas
        
    Raises:
        FileNotFoundError: Se o arquivo XML não for encontrado
        ET.ParseError: Se o XML estiver malformado
        
    Exemplo:
        >>> df = xml_para_dataframe(
        ...     'arquivo.xml',
        ...     'titprivado',
        ...     'isin',
        ...     'codativo',
        ...     'cnpjemissor'
        ... )
    """
    
    # ========================================================================
    # PASSO 1: PARSING DO ARQUIVO XML
    # ========================================================================
    try:
        # Faz o parsing do arquivo XML completo
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        print(f"✓ XML carregado com sucesso: {caminho_xml}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_xml}")
    except ET.ParseError as e:
        raise ET.ParseError(f"Erro ao fazer parsing do XML: {e}")
    
    
    # ========================================================================
    # PASSO 2: LOCALIZAÇÃO DO NÓ PRINCIPAL (FUNDO)
    # ========================================================================
    # Assumindo que a estrutura é: raiz > fundo > tags_pai
    fundo = root.find('fundo')
    
    if fundo is None:
        raise ValueError("Tag 'fundo' não encontrada no XML")
    
    
    # ========================================================================
    # PASSO 3: BUSCA DE TODAS AS OCORRÊNCIAS DA TAG PAI
    # ========================================================================
    # findall() retorna TODAS as ocorrências da tag especificada
    elementos_pai = fundo.findall(tag_pai)
    
    print(f"✓ Encontradas {len(elementos_pai)} ocorrências da tag '{tag_pai}'")
    
    if len(elementos_pai) == 0:
        print(f"⚠ Nenhuma ocorrência encontrada para a tag '{tag_pai}'")
        # Retorna DataFrame vazio com as colunas especificadas
        return pd.DataFrame(columns=list(tags_filhas))
    
    
    # ========================================================================
    # PASSO 4: EXTRAÇÃO DOS DADOS DAS TAGS FILHAS
    # ========================================================================
    # Dicionário para armazenar listas de valores de cada tag filha
    # Estrutura: {'tag_filha_A': [valor1, valor2, ...], 'tag_filha_B': [...]}
    dados: Dict[str, List[str]] = {tag: [] for tag in tags_filhas}
    
    # Itera sobre cada ocorrência da tag_pai
    for idx, elemento_pai in enumerate(elementos_pai, 1):
        
        # Para cada tag_filha especificada, busca seu valor
        for tag_filha in tags_filhas:
            
            # Busca o elemento da tag_filha dentro do elemento_pai atual
            elemento_filha = elemento_pai.find(tag_filha)
            
            if elemento_filha is not None:
                # EXTRAÇÃO DO TEXTO LIMPO
                # ---------------------------------------------------------------
                # Aqui está a lógica crucial: extrair_texto_limpo() utiliza
                # itertext() para capturar TODO o conteúdo textual do elemento,
                # incluindo texto de sub-elementos, ignorando as tags XML.
                # 
                # Exemplo:
                # <codativo>LFSC24000XU</codativo> → retorna 'LFSC24000XU'
                # <valor><num>123</num></valor> → retorna '123'
                # ---------------------------------------------------------------
                valor = extrair_texto_limpo(elemento_filha)
                dados[tag_filha].append(valor)
            else:
                # Se a tag_filha não existir nesta ocorrência, adiciona string vazia
                # Isso garante que todas as listas tenham o mesmo comprimento
                dados[tag_filha].append('')
    
    print(f"✓ Dados extraídos de {len(tags_filhas)} tags filhas")
    
    
    # ========================================================================
    # PASSO 5: CRIAÇÃO DO DATAFRAME PANDAS
    # ========================================================================
    # Utilizamos pd.DataFrame(dict) onde cada chave vira uma coluna
    # e cada lista de valores vira os dados dessa coluna
    # 
    # O Pandas automaticamente alinha os dados e preenche com NaN
    # caso as listas tenham tamanhos diferentes (embora neste script
    # garantimos que todas tenham o mesmo tamanho)
    df = pd.DataFrame(dados)
    
    print(f"✓ DataFrame criado com {len(df)} linhas e {len(df.columns)} colunas")
    print(f"  Colunas: {list(df.columns)}")
    
    return df


def exibir_info_dataframe(df: pd.DataFrame) -> None:
    """
    Exibe informações resumidas sobre o DataFrame criado.
    
    Args:
        df: DataFrame Pandas para análise
    """
    print("\n" + "="*70)
    print("INFORMAÇÕES DO DATAFRAME")
    print("="*70)
    print(f"\nDimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:")
    print(df.dtypes)
    print(f"\nValores nulos por coluna:")
    print(df.isnull().sum())
    print(f"\nPrimeiras 5 linhas:")
    print(df.head())
    print("="*70 + "\n")


# ============================================================================
# EXEMPLO DE USO
# ============================================================================
if __name__ == "__main__":
    
    # Definição dos parâmetros de entrada
    caminho_xml = r'S:\01-Back_Office\3 - Fundos, Carteiras e Clubes\1 - Fundos\19 - FI RF SOMMA Torino\4- Arquivos XML\2026\2026-02\FD28206220000195_20260209_20260210033437_SOMMA TORINO FIF CI RF CRED PRIV LP RESP LTDA_014392.XML'
    tag_pai = 'titprivado'
    
    # Tags filhas que queremos extrair
    tags_filhas = (
        'codativo',
        'qtdisponivel',
        'puposicao',
        'principal',
        'valorfindisp',
    )
    
    print("\n" + "="*70)
    print("INICIANDO EXTRAÇÃO DE DADOS DO XML")
    print("="*70 + "\n")
    
    # Executa a extração
    df = xml_para_dataframe(
        caminho_xml,
        tag_pai,
        *tags_filhas
    )
    
    # Exibe informações sobre o DataFrame criado
    exibir_info_dataframe(df)
    
    # Salva o DataFrame em CSV (opcional)
    output_csv = r'S:\01-Back_Office\9 - Pastas Pessoais\Angelo Carvalho\dados_extraidos.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✓ Dados salvos em: {output_csv}\n")
    
    # Exemplo com outra tag_pai
    print("\n" + "="*70)
    print("EXEMPLO 2: EXTRAINDO DADOS DE DEBÊNTURES")
    print("="*70 + "\n")
    
    df_debentures = xml_para_dataframe(
        caminho_xml,
        'debenture',
        'isin',
        'coddeb',
        'cnpjemissor',
        'qtdisponivel',
        'puposicao',
        'indexador',
        'coupom'
    )
    
    exibir_info_dataframe(df_debentures)
