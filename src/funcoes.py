import pandas as pd
import numpy as np
import csv
import re

def carregar_dados(filename: str):
    data_frame_dados = pd.read_csv(filename, sep=',')
    return data_frame_dados

def filtrar_generos(cabecalho, dados: pd.DataFrame):
    # Gêneros que queremos remover
    generos_indesejados = ['hentai', 'yaoi', 'yuri', 'ecchi', 'shota', 'loli', 'harem', 'reverse harem', 'josei']
    
    # Índice da coluna de gêneros
    indice_genero = cabecalho.index('genre')
    
    # Filtra as linhas que não contêm os gêneros indesejados
    dados_filtrados = [row for row in dados if not any(genero in row[indice_genero].lower() for genero in generos_indesejados)]
    
    return dados_filtrados

def limpar_dados(df: pd.DataFrame):
    # Remove linhas onde 'type' está vazio
    df = df[df['type'].notna()]
    # Atualiza 'episodes' para 1 onde 'type' é 'Movie' e 'episodes' é 'unknown'
    df.loc[(df['type'] == 'Movie') & (df['episodes'] == 'unknown'), 'episodes'] = 1
    # Remove linhas onde 'rating', 'genre', 'members' ou 'aired' estão vazios
    df = df[df['rating'].notna()]
    df = df[df['genre'].notna()]
    df = df[df['members'].notna()]
    df = df[df['aired'].notna()]
    return df

def trocar_index(data_frame: pd.DataFrame, novos_index: dict):
    data_frame.rename(columns= novos_index, inplace=True)
    return data_frame

def selecionar_colunas(data_frame: pd.DataFrame, index):
    filtred_data_frame = data_frame[index]
    return filtred_data_frame


def salvar_anime_csv(cabecalho, dados: pd.DataFrame, caminho='anime_filtrado.csv'):
    try:
        with open(caminho, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(cabecalho)  # Escreve o cabeçalho
            writer.writerows(dados)      # Escreve os dados filtrados
        print(f"Os dados filtrados foram salvos em '{caminho}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

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
