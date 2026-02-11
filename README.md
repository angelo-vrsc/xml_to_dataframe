Script Python especializado para extrair dados de arquivos XML e transformá-los em DataFrames Pandas, com foco em estruturas hierárquicas de fundos de investimento.

## aracterísticas Principais

- **Extração de Texto Limpo**: Utiliza `itertext()` para capturar conteúdo textual ignorando tags XML internas
- **Flexibilidade**: Aceita múltiplas tags filhas como parâmetros
- **Robustez**: Tratamento de erros e validações
- **Alinhamento Automático**: Pandas gerencia tamanhos diferentes de listas
- **Documentação Completa**: Código totalmente comentado

##  Como Usar

### Sintaxe Básica

```python
from xml_to_dataframe import xml_para_dataframe

df = xml_para_dataframe(
    caminho_xml,     # Path do arquivo XML
    tag_pai,         # Tag de segunda ordem (ex: 'titprivado')
    *tags_filhas     # Tags cujos valores serão extraídos
)
```

### Extrair Títulos Privados

```python
df_titulos = xml_para_dataframe(
    'arquivo.xml',
    'titprivado',
    'isin',
    'codativo',
    'cnpjemissor',
    'qtdisponivel',
    'puposicao',
    'principal',
    'indexador',
    'coupom'
)

print(df_titulos.head())
```

### Exemplo 2: Extrair Debêntures

```python
df_debentures = xml_para_dataframe(
    'arquivo.xml',
    'debenture',
    'isin',
    'coddeb',
    'cnpjemissor',
    'qtdisponivel',
    'puposicao',
    'indexador',
    'coupom'
)
```

### Exemplo 3: Extrair Header

```python
df_header = xml_para_dataframe(
    'arquivo.xml',
    'header',
    'isin',
    'cnpj',
    'nome',
    'dtposicao',
    'patliq',
    'valorcota'
)
```

### Exemplo 4: Extrair Cotas

```python
df_cotas = xml_para_dataframe(
    'arquivo.xml',
    'cotas',
    'isin',
    'cnpjfundo',
    'qtdisponivel',
    'puposicao',
    'nivelrsc'
)
```

## Estrutura do XML Esperada

```xml
<arquivoposicao_4_01>
  <fundo>
    <header>
      <isin>BRSMM7CTF009</isin>
      <cnpj>28206220000195</cnpj>
      ...
    </header>
    <titprivado>
      <isin>BRABCBLFN6Z8</isin>
      <codativo>LFSC24000XU</codativo>
      ...
    </titprivado>
    <titprivado>
      ...
    </titprivado>
    <debenture>
      ...
    </debenture>
  </fundo>
</arquivoposicao_4_01>
```

##  Funções Disponíveis

### `xml_para_dataframe(caminho_xml, tag_pai, *tags_filhas)`

Função principal que extrai dados do XML.

**Parâmetros:**
- `caminho_xml` (str): Caminho completo do arquivo XML
- `tag_pai` (str): Tag de segunda ordem que agrupa os dados
- `*tags_filhas` (str): Tags cujos valores serão extraídos (aceita múltiplas)

**Retorna:**
- `pd.DataFrame`: DataFrame com colunas nomeadas conforme as tags_filhas

**Exceções:**
- `FileNotFoundError`: Arquivo XML não encontrado
- `ET.ParseError`: XML malformado
- `ValueError`: Tag 'fundo' não encontrada

### `extrair_texto_limpo(elemento)`

Extrai texto limpo de um elemento XML, incluindo sub-elementos.

**Parâmetros:**
- `elemento` (ET.Element): Elemento XML

**Retorna:**
- `str`: Texto limpo sem tags

### `exibir_info_dataframe(df)`

Exibe informações resumidas sobre o DataFrame.

**Parâmetros:**
- `df` (pd.DataFrame): DataFrame para análise

## Notas Importantes

1. **Extração de Texto**: O método `itertext()` garante que apenas dados brutos sejam coletados, ignorando estruturas XML internas.

2. **Valores Vazios**: Se uma tag filha não existir em determinada ocorrência, uma string vazia é inserida para manter o alinhamento.

3. **Tipos de Dados**: Todos os valores são extraídos como strings. Para conversão de tipos, use:
   ```python
   df['qtdisponivel'] = pd.to_numeric(df['qtdisponivel'])
   df['dtemissao'] = pd.to_datetime(df['dtemissao'], format='%Y%m%d')
   ```

4. **Performance**: O script é otimizado para arquivos XML de tamanho médio (até 10MB).

## Exportação de Dados

```python
# Exportar para CSV
df.to_csv('output.csv', index=False, encoding='utf-8-sig')

# Exportar para Excel
df.to_excel('output.xlsx', index=False)

# Exportar para JSON
df.to_json('output.json', orient='records', force_ascii=False)

# Exportar para Parquet
df.to_parquet('output.parquet', index=False)
```

## 🔍 Análise de Dados Extraídos

```python
# Verificar valores únicos
print(df['indexador'].value_counts())

# Estatísticas descritivas
print(df.describe())

# Filtrar dados
df_cdi = df[df['indexador'] == 'CDI']

# Agrupar dados
df_agrupado = df.groupby('cnpjemissor')['principal'].sum()
```

## Dependências

```
pandas>=1.3.0
```

## Troubleshooting

### Erro: "Tag 'fundo' não encontrada"
- Verifique se a estrutura do XML está correta
- Certifique-se de que o nó raiz contém um filho chamado 'fundo'

### Erro: "Nenhuma ocorrência encontrada"
- Verifique se o nome da `tag_pai` está correto
- Confirme que existem ocorrências dessa tag no XML

### Valores vazios no DataFrame
- Isso é esperado quando uma tag filha não existe em determinada ocorrência
- Use `df.fillna()` ou `df.replace()` para tratar valores vazios

## Suporte

Para dúvidas ou problemas, verifique:
1. Se o arquivo XML está bem formado
2. Se os nomes das tags estão corretos (case-sensitive)
3. Se as dependências estão instaladas

****
