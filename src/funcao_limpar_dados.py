import pandas as pd
import re
import numpy as np
from funcoes import *  # Certifique-se de que as funções necessárias estão no arquivo funcoes.py
import sys 

# Função para abrir o arquivo anime.csv e ler os dados.
def abrir_anime_csv(caminho='../data/anime.csv'):
    """
    Lê o arquivo CSV de animes e retorna um DataFrame do Pandas.

    Parâmetros
    ----------
    caminho : str, opcional
        O caminho para o arquivo CSV (padrão é '../data/anime.csv').

    Retorna
    -------
    DataFrame
        Um DataFrame contendo os dados do arquivo CSV.

    Exceções
    ---------
    FileNotFoundError
        Se o arquivo especificado não for encontrado.
    Exception
        Para qualquer erro durante a leitura do arquivo.
    """
    try:
        # Lê o arquivo CSV diretamente com Pandas
        df = pd.read_csv(caminho, encoding='ISO-8859-1', sep=',')
        print(f"Cabeçalho do arquivo: {df.columns.tolist()}")  # Imprime o cabeçalho para inspeção
        return df
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
        return None  # Retorna None se houver erro
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Função para filtrar os gêneros indesejados.
def filtrar_generos(df):
    """
    Filtra os gêneros indesejados do DataFrame de animes.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame original com os dados dos animes.

    Retorna
    -------
    DataFrame
        Um DataFrame contendo apenas animes que não possuem os gêneros indesejados.
    """
    generos_indesejados = ['hentai', 'yaoi', 'yuri', 'ecchi', 'shota', 'loli', 'harem', 'reverse harem', 'josei']

    # Filtra as linhas que não contêm os gêneros indesejados
    mask = ~df['genre'].str.lower().str.contains('|'.join(generos_indesejados), na=False)
    dados_filtrados = df[mask]

    return dados_filtrados

# Função para converter datas para o formato DD/MM/YYYY.
def convert_date(date_str):
    """
    Converte uma string de data no formato 'Mmm DD, YYYY' para 'DD/MM/YYYY'.

    Parâmetros
    ----------
    date_str : str
        A string de data a ser convertida.

    Retorna
    -------
    str ou None
        A data convertida no formato 'DD/MM/YYYY', ou None se a conversão falhar.
    """
    match = re.match(r'(\w{3}) (\d{1,2}), (\d{4})', date_str)
    if match:
        month_str, day, year = match.groups()
        month_mapping = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        month = month_mapping.get(month_str)
        return f"{day.zfill(2)}/{month}/{year}"
    return None

# Função para adicionar as datas do arquivo animes_complemento.csv.
def adicionar_datas(anime):
    """
    Adiciona a coluna de datas ao DataFrame de animes com base em um arquivo complementar.

    Parâmetros
    ----------
    anime : DataFrame
        O DataFrame contendo os dados dos animes.

    Retorna
    -------
    DataFrame
        O DataFrame atualizado com a coluna de datas adicionada.
    """
    try:
        animes_complemento = abrir_anime_csv('/Python/projeto/Trabalho_LP_A1/data/animes_complemento.csv')
        print("Colunas em animes_complemento:", animes_complemento.columns.tolist())
    except Exception as e:
        print(f"Erro ao ler animes_complemento.csv: {e}")
        return anime

    # Renomeia 'anime_id' para 'uid' no DataFrame principal se necessário
    if 'anime_id' in anime.columns:
        anime = anime.rename(columns={'anime_id': 'uid'})

    # Cria a coluna 'aired' se não existir
    if 'aired' not in anime.columns:
        anime['aired'] = None

    # Adiciona a data do animes_complemento para cada anime em anime_filtrado
    for index, row in anime.iterrows():
        uid = row['uid']
        matching_row = animes_complemento[animes_complemento['uid'] == uid]
        if not matching_row.empty:
            aired_value = matching_row['aired'].values[0]
            if pd.notna(aired_value) and isinstance(aired_value, str):
                first_date = aired_value.split(' to ')[0]
                converted_date = convert_date(first_date)
                if converted_date:
                    anime.at[index, 'aired'] = converted_date

    return anime

# Função para preencher episódios "unknown".
def preencher_episodios_unknown(anime):
    """
    Preenche os valores "unknown" na coluna de episódios com dados de um DataFrame de animes limpos.

    Parâmetros
    ----------
    anime : DataFrame
        O DataFrame contendo os dados dos animes.

    Retorna
    -------
    DataFrame
        O DataFrame atualizado com os episódios preenchidos.
    """
    anime_cleaned = abrir_anime_csv('/Python/projeto/Trabalho_LP_A1/data/anime_cleaned.csv')

    # Renomeia 'anime_id' para 'uid' no DataFrame cleaned
    if 'anime_id' in anime_cleaned.columns:
        anime_cleaned = anime_cleaned.rename(columns={'anime_id': 'uid'})

    # Mescla os DataFrames para preencher os episódios "unknown"
    anime = anime.merge(anime_cleaned[['uid', 'episodes']], on='uid', how='left', suffixes=('', '_cleaned'))
    
    # Preenche os episódios unknown
    anime['episodes'] = anime.apply(lambda row: row['episodes_cleaned'] if row['episodes'] == 'unknown' else row['episodes'], axis=1)

    # Remove a coluna auxiliar
    anime.drop(columns=['episodes_cleaned'], inplace=True)

    return anime

# Função para limpar os dados finais.
def limpar_dados(df):
    """
    Limpa o DataFrame, removendo entradas inválidas e preenchendo valores padrão.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame a ser limpo.

    Retorna
    -------
    DataFrame
        O DataFrame limpo.
    """
    df = df[df['type'].notna()]
    df.loc[(df['type'] == 'Movie') & (df['episodes'] == 'unknown'), 'episodes'] = 1
    df = df[df['rating'].notna()]
    df = df[df['genre'].notna()]
    df = df[df['members'].notna()]
    df = df[df['aired'].notna()]
    return df

# Função para remover linhas com episódios "unknown".
def remover_unknown(df):
    """
    Remove linhas do DataFrame que têm episódios marcados como "unknown".

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame a ser filtrado.

    Retorna
    -------
    DataFrame
        O DataFrame sem as linhas que têm episódios "unknown".
    """
    return df[df['episodes'].str.lower() != 'unknown']

# Função para salvar o arquivo final como anime_filtrado_limpo.csv.
def salvar_anime_csv(df, caminho='../data/anime_filtrado_limpo.csv'):
    """
    Salva o DataFrame em um arquivo CSV.

    Parâmetros
    ----------
    df : DataFrame
        O DataFrame a ser salvo.
    caminho : str, opcional
        O caminho para salvar o arquivo (padrão é '../data/anime_filtrado_limpo.csv').

    Exceções
    ---------
    Exception
        Para qualquer erro durante o salvamento do arquivo.
    """
    try:
        df.to_csv(caminho, index=False, encoding='ISO-8859-1')
        print(f"Arquivo salvo com sucesso em {caminho}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# Função principal para integrar todas as partes.
def processar_anime():
    """
    Função principal que coordena o processamento dos dados dos animes.

    Realiza as seguintes etapas:
    1. Lê o arquivo anime.csv.
    2. Filtra os gêneros indesejados.
    3. Adiciona as datas a partir do animes_complemento.csv.
    4. Preenche episódios desconhecidos.
    5. Limpa os dados finais.
    6. Remove linhas com episódios "unknown".
    7. Salva o DataFrame final em anime_filtrado_limpo.csv.
    """
    anime_data = abrir_anime_csv()

    if anime_data is not None:
        # Carrega o arquivo 'anime.csv' e filtra gêneros indesejados
        anime_data_filtrado = filtrar_generos(anime_data)
        
        # Adiciona as datas de 'animes_complemento.csv'
        anime_data_completo = adicionar_datas(anime_data_filtrado)

        # Preenche episódios desconhecidos
        anime_data_completo = preencher_episodios_unknown(anime_data_completo)

        # Limpa os dados finais
        anime_data_limpo = limpar_dados(anime_data_completo)

        # Remove linhas com episódios "unknown"
        anime_data_final = remover_unknown(anime_data_limpo)

        # Salva o DataFrame final em um novo arquivo
        salvar_anime_csv(anime_data_final)

# Executa o processo
if __name__ == "__main__":
    processar_anime()
