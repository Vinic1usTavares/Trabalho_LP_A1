#Hipotese 3
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def extrair_ano(data_str):
    """
    Extracts the year from a date string in the format 'DD/MM/YYYY'.

    Parameters
    ----------
    data_str : str
        A string representing the date in 'DD/MM/YYYY' format.

    Returns
    -------
    int or None
        The year extracted from the date string. Returns None if the date string
        cannot be parsed.

    Examples
    --------
    >>> extrair_ano('12/08/2015')
    2015

    >>> extrair_ano('invalid date')
    None
    """
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y").year
    except (ValueError, TypeError):
        return None


def analisar_hipotese(arquivo_csv):
    """
    Analyzes the correlation between the release year of anime and its popularity,
    measured by the number of members, for the hypothesis that recently released
    anime tend to be more popular.

    The analysis generates two visualizations:
    1. A scatter plot showing the relationship between the release year and the number
       of members (popularity), differentiating recent (2010-2017) from older anime.
    2. A bar chart showing the average number of members per 10-year interval of release.

    Parameters
    ----------
    arquivo_csv : str
        Path to the CSV file containing anime data. The dataset should include
        the columns 'aired' (release date in DD/MM/YYYY format), 'rating' (user
        rating), and 'members' (popularity measure).

    Returns
    -------
    tuple of str
        A tuple containing two file paths of the generated visualizations:
        - `ano_vs_membros_combinado.png`: A scatter plot showing the relationship
          between release year and member count, differentiating between recent (2010-2017)
          and non-recent anime, and including a trendline for the average members per year.
        - `membros_medio_por_intervalo.png`: A bar chart showing the average number
          of members grouped by 10-year release intervals.

    Notes
    -----
    - The function assumes the 'aired' column contains dates in the format 'DD/MM/YYYY'.
      If a date cannot be parsed, it is treated as missing data.
    - The dataset's release years are split into two groups: anime released from 2010 to
      2017 (considered recent) and anime released before 2010 (non-recent).
    - The scatter plot includes a vertical line at 2010, marking the distinction between
      recent and non-recent anime, and a trendline for the average number of members per year.
    - The bar chart groups the number of members by 10-year intervals, starting from 1940,
      and plots the average number of members for each interval.
    - The plots are saved in the `/Python/projeto/Trabalho_LP_A1/data/` directory.

    Examples
    --------
    >>> analisar_hipotese('/Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv')
    ('/Python/projeto/Trabalho_LP_A1/data/ano_vs_membros_combinado.png',
     '/Python/projeto/Trabalho_LP_A1/data/membros_medio_por_intervalo.png')

    Raises
    ------
    FileNotFoundError
        If the provided CSV file does not exist.
    ValueError
        If required columns ('aired', 'members') are missing from the dataset.
    """
    
    # Carregar os dados do arquivo CSV
    anime_df = pd.read_csv(arquivo_csv, encoding='ISO-8859-1', sep=',')
    
    # Verificação de colunas necessárias
    if 'aired' not in anime_df.columns or 'members' not in anime_df.columns:
        raise ValueError("O arquivo CSV deve conter as colunas 'aired' e 'members'.")

    # Extrair o ano da coluna 'aired'
    anime_df['ano'] = anime_df['aired'].apply(extrair_ano)

    # Converter as colunas relevantes para tipos numéricos
    anime_df['ano'] = pd.to_numeric(anime_df['ano'], errors='coerce')
    anime_df['rating'] = pd.to_numeric(anime_df['rating'], errors='coerce')
    anime_df['members'] = pd.to_numeric(anime_df['members'], errors='coerce')

    # Definir ano limite para animes recentes e ano máximo no dataset
    ano_limite = 2010
    ano_maximo = 2017  # Data limite do dataset

    # Gráfico combinado: Animes recentes vs. não recentes
    plt.figure(figsize=(12, 6))

    # Selecionar e plotar animes recentes (>= 2010)
    animes_recentes = anime_df[anime_df['ano'] >= ano_limite]
    plt.scatter(animes_recentes['ano'], animes_recentes['members'], 
                alpha=0.5, color='blue', label='Animes Recentes (2010-2017)')

    # Selecionar e plotar animes não recentes (< 2010)
    animes_nao_recentes = anime_df[anime_df['ano'] < ano_limite]
    plt.scatter(animes_nao_recentes['ano'], animes_nao_recentes['members'], 
                alpha=0.5, color='gray', label='Animes Não Recentes (Antes de 2010)')
    
    # Adicionar linha vertical no limiar de 2010
    plt.axvline(x=ano_limite, color='red', linestyle='--', label='Limiar de 2010')

    # Calcular e plotar a média do número de membros por ano
    media_membros_por_ano = anime_df.groupby('ano')['members'].mean().dropna()
    plt.plot(media_membros_por_ano.index, media_membros_por_ano, color='yellow', label='Média de Membros por Ano')

    # Configurações do gráfico
    plt.title('Ano de Lançamento vs. Número de Membros (Até 2017)')
    plt.xlabel('Ano de Lançamento')
    plt.ylabel('Número de Membros')
    plt.grid(True)
    plt.xlim(anime_df['ano'].min(), ano_maximo)
    plt.ylim(0, anime_df['members'].max() * 1.1)
    plt.legend()
    plt.savefig('/Python/projeto/Trabalho_LP_A1/data/ano_vs_membros_combinado.png')
    plt.close()

    # Gráfico de barras: Número médio de membros por intervalo de lançamento
    plt.figure(figsize=(12, 6))
    bins = np.arange(1940, 2020, 10)  # Intervalos de 10 anos, começando em 1940
    labels = [f'{i}-{i+10}' for i in bins[:-1]]  # Rótulos dos intervalos
    
    # Adicionar a coluna de intervalo ao DataFrame
    anime_df['intervalo'] = pd.cut(anime_df['ano'], bins=bins, right=False, labels=labels)

    # Calcular a média de membros por intervalo de lançamento
    media_membros = anime_df.groupby('intervalo')['members'].mean()

    # Criar gráfico de barras
    media_membros.plot(kind='bar', color='cyan')
    plt.title('Número Médio de Membros por Intervalo de Lançamento')
    plt.xlabel('Intervalo de Lançamento')
    plt.ylabel('Número Médio de Membros')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.savefig('/Python/projeto/Trabalho_LP_A1/data/membros_medio_por_intervalo.png')
    plt.close()

    # Retornar os caminhos dos arquivos gerados
    return (
        '/Python/projeto/Trabalho_LP_A1/data/ano_vs_membros_combinado.png',
        '/Python/projeto/Trabalho_LP_A1/data/membros_medio_por_intervalo.png'
    )


# Executar a função, se este arquivo for executado como script principal
if __name__ == "__main__":
    arquivo = '/Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv'
    analisar_hipotese(arquivo)
