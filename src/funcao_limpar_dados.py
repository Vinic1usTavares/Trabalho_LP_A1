import pandas as pd
import re
import numpy as np
from funcoes import *  # Certifique-se de que as funções necessárias estão no arquivo funcoes.py

# Função para abrir o arquivo anime.csv e ler os dados
def abrir_anime_csv(caminho='../data/anime.csv'):
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

# Função para filtrar os gêneros indesejados
def filtrar_generos(df):
    generos_indesejados = ['hentai', 'yaoi', 'yuri', 'ecchi', 'shota', 'loli', 'harem', 'reverse harem', 'josei']

    # Filtra as linhas que não contêm os gêneros indesejados
    mask = ~df['genre'].str.lower().str.contains('|'.join(generos_indesejados), na=False)
    dados_filtrados = df[mask]

    return dados_filtrados

# Função para converter datas para o formato DD/MM/YYYY
def convert_date(date_str):
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

# Função para adicionar as datas do arquivo animes_complemento.csv
def adicionar_datas(anime):
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

# Função para preencher episódios "unknown"
def preencher_episodios_unknown(anime):
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

# Função para limpar os dados finais
def limpar_dados(df):
    df = df[df['type'].notna()]
    df.loc[(df['type'] == 'Movie') & (df['episodes'] == 'unknown'), 'episodes'] = 1
    df = df[df['rating'].notna()]
    df = df[df['genre'].notna()]
    df = df[df['members'].notna()]
    df = df[df['aired'].notna()]
    return df

# Função para remover linhas com episódios "unknown"
def remover_unknown(df):
    return df[df['episodes'].str.lower() != 'unknown']

# Função para salvar o arquivo final como anime_filtrado_limpo.csv
def salvar_anime_csv(df, caminho='../data/anime_filtrado_limpo.csv'):
    try:
        df.to_csv(caminho, index=False, encoding='ISO-8859-1')
        print(f"Arquivo salvo com sucesso em {caminho}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# Função principal para integrar todas as partes
def processar_anime():
    anime_data = abrir_anime_csv()

    if anime_data is not None:
        # Carrega o arquivo 'anime.csv' e filtra os gêneros indesejados
        anime_data = abrir_anime_csv('/Python/projeto/Trabalho_LP_A1/data/anime.csv') 

        # Filtra os gêneros indesejados
        anime_data_filtrado = filtrar_generos(anime_data)

        # Adiciona as datas usando o animes_complemento.csv
        anime_filtrado = adicionar_datas(anime_data_filtrado)

        # Preenche episódios unknown
        anime_filtrado = preencher_episodios_unknown(anime_filtrado)

        # Limpa os dados finais
        anime_filtrado_limpo = limpar_dados(anime_filtrado)

        # Remove todas as linhas com episódios "unknown" usando a nova função
        anime_filtrado_limpo = remover_unknown(anime_filtrado_limpo)

        # Salva o arquivo final
        salvar_anime_csv(anime_filtrado_limpo, caminho='/Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv')
        
        print("Arquivo processado com sucesso.")

if __name__ == "__main__":
    processar_anime()
