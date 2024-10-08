import pandas as pd
import re
from funcoes import*

# Função para abrir o arquivo anime.csv e ler os dados
def abrir_anime_csv(caminho='../data/anime.csv'):
    try:
        # Lê o arquivo CSV diretamente com Pandas
        df = pd.read_csv(caminho, encoding='ISO-8859-1', sep=';')
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

# Função para salvar os dados filtrados
def salvar_anime_csv(df, caminho='anime_filtrado.csv'):
    try:
        df.to_csv(caminho, index=False, encoding='ISO-8859-1', sep=';')  # Salva com o mesmo encoding e delimitador
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
        animes_complemento = pd.read_csv('animes_complemento.csv', encoding='latin1', sep=';', on_bad_lines='skip')
        print("Colunas em animes_complemento:", animes_complemento.columns.tolist())
    except Exception as e:
        print(f"Erro ao ler animes_complemento.csv: {e}")
        return anime_filtrado

    # Cria a coluna 'aired' se não existir
    if 'aired' not in anime_filtrado.columns:
        anime_filtrado['aired'] = None

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
    anime_data = abrir_anime_csv()

    if anime_data is not None:
        # Filtra os gêneros indesejados
        anime_data_filtrado = filtrar_generos(anime_data)
        salvar_anime_csv(anime_data_filtrado)

        # Carrega o anime filtrado como DataFrame para adicionar as datas
        anime_filtrado = pd.read_csv('anime_filtrado.csv', encoding='ISO-8859-1', sep=';')
        anime_filtrado = adicionar_datas(anime_filtrado)
        data_frame_complementar = carregar_dados('./data/animes_complemento.csv')
        data_frame_complementar = limpar_dados(data_frame_complementar)

        novos_index ={
        'uid':'id',
        'rating':'score'
        }
        data_frame_principal = trocar_index(data_frame_principal, novos_index)
        data_frame_complementar = selecionar_colunas(data_frame_complementar, ['uid','title','genre','episodes','score','members'])
        data_frame_complementar = pd.merge(data_frame_principal,data_frame_complementar, on='episodes',how='outer')
        data_frame_complementar = data_frame_complementar[data_frame_complementar['episodes'] != 'Unknown']
        data_frame_complementar['episodes'] = pd.to_numeric(data_frame_complementar['episodes'], errors='coerce')
        data_frame_complementar = data_frame_complementar[data_frame_complementar['episodes'] != np.nan]


        # Limpa os dados finais
        anime_filtrado_limpo = limpar_dados(anime_filtrado)
        

        # Salva o arquivo final limpo
        anime_filtrado_limpo.to_csv('anime_filtrado_limpo.csv', index=False, encoding='ISO-8859-1', sep=';')
        print("Arquivo 'anime_filtrado_limpo.csv' gerado com sucesso.")

if __name__ == "__main__":
    processar_anime()
