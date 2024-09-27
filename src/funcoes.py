import pandas as pd
import numpy as np

def carregar_dados(filename: str):
    data_frame_dados = pd.read_csv(filename, sep=',')
    return data_frame_dados

def filtrar_generos(cabecalho, dados):
    # Gêneros que queremos remover
    generos_indesejados = ['hentai', 'yaoi', 'yuri', 'ecchi', 'shota', 'loli', 'harem', 'reverse harem', 'josei']
    
    # Índice da coluna de gêneros
    indice_genero = cabecalho.index('genre')
    
    # Filtra as linhas que não contêm os gêneros indesejados
    dados_filtrados = [row for row in dados if not any(genero in row[indice_genero].lower() for genero in generos_indesejados)]
    
    return dados_filtrados

def limpar_dados(data_frame, colunas = False):
    data_frame = data_frame.drop_duplicates() 
    if colunas:
        data_frame.drop(colunas, axis=1, inplace=True)
    return data_frame

def trocar_index(data_frame: pd.DataFrame, novos_index: dict):
    data_frame.rename(columns= novos_index, inplace=True)
    return data_frame

def selecionar_colunas(data_frame: pd.DataFrame, index):
    filtred_data_frame = data_frame[index]
    return filtred_data_frame

def completar_dados(data_frame_principal: pd.DataFrame, data_frame_complementar: pd.DataFrame, index: str, valor: str):
    data_frame_principal[index,valor].fillna(data_frame_complementar.loc[index,valor])
    return data_frame_principal
