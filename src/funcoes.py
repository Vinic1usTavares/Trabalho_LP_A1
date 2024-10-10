import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import re

# Função para extrair o ano do campo 'aired' no formato DD/MM/YYYY
def extrair_ano(data_str):
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y").year
    except (ValueError, TypeError):
        return None
    
# Função para abrir o arquivo anime.csv e ler os dados
def abrir_anime_csv(caminho='./data/anime.csv'):
    try:
        # Lê o arquivo CSV diretamente com Pandas
        df = pd.read_csv(caminho, encoding='ISO-8859-1', sep=';')
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

# Função para salvar os dados filtrados
def salvar_anime_csv(df, caminho='./data/anime_filtrado.csv'):
    try:
        df.to_csv(caminho, index=False, encoding='ISO-8859-1', sep=',')  # Salva com o mesmo encoding e delimitador
        print(f"Os dados filtrados foram salvos em '{caminho}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

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
def adicionar_datas(anime_filtrado):
    try:
        animes_complemento = pd.read_csv('./data/animes_complemento.csv', encoding='latin1', sep=';', on_bad_lines='skip')
        print("Colunas em animes_complemento:", animes_complemento.columns.tolist())
    except Exception as e:
        print(f"Erro ao ler animes_complemento.csv: {e}")
        return anime_filtrado

    # Cria a coluna 'aired' se não existir
    if 'aired' not in anime_filtrado.columns:
        anime_filtrado.loc[:, 'aired'] = None


    # Adiciona a data do animes_complemento para cada anime em anime_filtrado
    for index, row in anime_filtrado.iterrows():
        id = row['id']
        matching_row = animes_complemento[animes_complemento['id'] == id]
        if not matching_row.empty:
            aired_value = matching_row['aired'].values[0]
            if pd.notna(aired_value) and isinstance(aired_value, str):
                first_date = aired_value.split(' to ')[0]
                converted_date = convert_date(first_date)
                if converted_date:
                    anime_filtrado.at[index, 'aired'] = converted_date

    return anime_filtrado

# Função para limpar os dados finais
def limpar_dados(df):
    df = df[df['type'].notna()]
    df.loc[(df['type'] == 'Movie') & (df['episodes'] == 'unknown'), 'episodes'] = 1
    df = df[df['rating'].notna()]
    df = df[df['genre'].notna()]
    df = df[df['members'].notna()]
    df = df[df['aired'].notna()]
    return df

# Função principal para integrar todas as partes
def processar_anime():
    anime_data = abrir_anime_csv(caminho='./data/anime.csv')

    if anime_data is not None:
        # Filtra os gêneros indesejados
        anime_filtrado = filtrar_generos(anime_data)
        #salvar_anime_csv(anime_filtrado)

        # Carrega o anime filtrado como DataFrame para adicionar as datas
        #anime_filtrado = pd.read_csv('anime_filtrado.csv', encoding='ISO-8859-1', sep=';')
        anime_filtrado = adicionar_datas(anime_filtrado)
        data_frame_complementar = pd.read_csv('./data/anime_cleaned.csv',sep=',')

        novos_index ={
            'id':'anime_id'
        }
        anime_filtrado.rename(columns=novos_index, inplace=True)
        
        # Selecionando as colunas que nos interessam
        data_frame_complementar = data_frame_complementar[['anime_id','episodes']]
        # Conversão do tipo da coluna episódio para poder dar merge
        anime_filtrado.loc[:,'episodes'] = anime_filtrado['episodes'].astype(str)
        data_frame_complementar.loc[:,'episodes'] = data_frame_complementar['episodes'].astype(str)
        data_frame_complementar.rename(columns={'episodes': 'episodes_complementar'}, inplace=True)
        data_frame_final = pd.merge(anime_filtrado,data_frame_complementar, on='anime_id',how='left')
        data_frame_final.loc[:,'episodes'] = data_frame_final['episodes'].replace('Unknown', np.nan)
        data_frame_final['episodes'] = data_frame_final['episodes'].combine_first(data_frame_final['episodes_complementar'])
        data_frame_final.drop(columns=['episodes_complementar'], inplace=True)
        data_frame_final.dropna(inplace=True)
        data_frame_final.drop_duplicates(subset='anime_id', keep='first',inplace=True)
        data_frame_final = data_frame_final[data_frame_final['episodes'] != '0']


        # Limpa os dados finais
        data_frame_final = limpar_dados(data_frame_final)
        print(data_frame_final)
        

        # Salva o arquivo final limpo
        data_frame_final.to_csv('./data/data_frame_final.csv', index=False, encoding='ISO-8859-1', sep=';')
        print("Arquivo 'data_frame_final.csv' gerado com sucesso.")

# Função para analisar a correlação e gerar gráficos
def analisar_hipotese(arquivo_csv):
    # Carregar os dados do arquivo
    anime_df = pd.read_csv(arquivo_csv, encoding='ISO-8859-1', sep=';')
     
    # Extrair o ano da coluna 'aired'
    anime_df['ano'] = anime_df['aired'].apply(extrair_ano)
    
    # Converter as colunas relevantes para tipos numéricos
    anime_df['ano'] = pd.to_numeric(anime_df['ano'], errors='coerce')
    anime_df['rating'] = pd.to_numeric(anime_df['rating'], errors='coerce')
    anime_df['members'] = pd.to_numeric(anime_df['members'], errors='coerce')
    
    # Calcular correlação entre ano e número de membros
    correlacao_membros = anime_df['ano'].corr(anime_df['members'])
    print(f"Correlação entre ano de lançamento e número de membros: {correlacao_membros}")
    
    # Calcular correlação entre ano e nota (rating)
    correlacao_rating = anime_df['ano'].corr(anime_df['rating'])
    print(f"Correlação entre ano de lançamento e nota (rating): {correlacao_rating}")
    
    # Gráfico: Ano de lançamento x Número de membros
    plt.figure(figsize=(10, 6))
    plt.scatter(anime_df['ano'], anime_df['members'], alpha=0.5)
    plt.title('Ano de lançamento vs. Número de membros')
    plt.xlabel('Ano de lançamento')
    plt.ylabel('Número de membros')
    plt.grid(True)
    plt.savefig('ano_vs_membros.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos
    
    # Gráfico: Ano de lançamento x Nota (rating)
    plt.figure(figsize=(10, 6))
    plt.scatter(anime_df['ano'], anime_df['rating'], alpha=0.5, color='orange')
    plt.title('Ano de lançamento vs. Nota (rating)')
    plt.xlabel('Ano de lançamento')
    plt.ylabel('Nota (rating)')
    plt.grid(True)
    plt.savefig('ano_vs_rating.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos

    # Retornar o nome dos arquivos gerados
    return 'ano_vs_membros.png', 'ano_vs_rating.png'

# Executar a função
'''if __name__ == "__main__":
    arquivo = '/Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv'
    analisar_hipotese(arquivo)
'''