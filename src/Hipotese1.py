#Hipotese 1
import pandas as pd
import matplotlib.pyplot as plt
import os

def analisar_generos_populares(anime_data: pd.DataFrame):
    """
    Analisa a relação entre a nota e o número de membros para animes de gêneros populares e outros gêneros.
    
    São gerados gráficos de dispersão e gráficos de barras comparando o número médio de membros 
    para diferentes intervalos de notas em animes de gêneros populares e de outros gêneros.

    Parameters
    ----------
    anime_data : DataFrame
        DataFrame contendo as informações dos animes, incluindo as colunas 'rating', 'members' e 'genre'.
    
    Returns
    -------
    None
        Gera gráficos salvos em arquivos e não retorna nenhum valor.
    
    Gêneros Populares
    ----------------
    Os seguintes gêneros são considerados populares:
    - Fight
    - Sports
    - Shounen
    - Action
    - Isekai
    - Fantasy
    - Adventure

    Arquivos Gerados
    ----------------
    Serão salvos os seguintes gráficos:
    - relacao_notas_membros_generos_populares.png: Relação entre nota e número de membros para animes de gêneros populares.
    - relacao_notas_membros_outros_generos.png: Relação entre nota e número de membros para animes de outros gêneros.
    - media_membros_por_intervalo_notas.png: Número médio de membros por intervalo de notas, comparando gêneros populares e outros gêneros.
    """
    # Definindo os gêneros populares
    generos_populares = ["Fight", "Sports", "Shounen", "Action", "Isekai", "Fantasy", "Adventure"]

    # Filtrando os animes de gêneros populares
    anime_populares = anime_data[anime_data['genre'].str.contains('|'.join(generos_populares), case=False, na=False)]
    
    # Filtrando os animes de outros gêneros
    anime_outros = anime_data[~anime_data['genre'].str.contains('|'.join(generos_populares), case=False, na=False)]

    # Verificar os valores únicos na coluna 'rating' para garantir que eles estejam na faixa correta
    print("Valores únicos de rating (Gêneros Populares):", anime_populares['rating'].unique())
    print("Valores únicos de rating (Outros Gêneros):", anime_outros['rating'].unique())

    # Gráfico para Gêneros Populares
    plt.figure(figsize=(12, 8))
    plt.scatter(anime_populares['rating'], anime_populares['members'], color='blue', alpha=0.7)
    plt.title('Relação entre Nota e Número de Membros para Animes de Gêneros Populares')
    plt.xlabel('Nota (0-10)')
    plt.ylabel('Número de Membros')
    plt.xlim(0, 10)
    plt.ylim(0, anime_data['members'].max() * 1.1)
    plt.savefig('./data/dados_hipotese1/relacao_notas_membros_generos_populares.png')
    plt.close()
    print("Gráfico de relação entre notas e número de membros (Gêneros Populares) salvo.")

    # Gráfico para Outros Gêneros
    plt.figure(figsize=(12, 8))
    plt.scatter(anime_outros['rating'], anime_outros['members'], color='gray', alpha=0.5)
    plt.title('Relação entre Nota e Número de Membros para Animes de Outros Gêneros')
    plt.xlabel('Nota (0-10)')
    plt.ylabel('Número de Membros')
    plt.xlim(0, 10)
    plt.ylim(0, anime_data['members'].max() * 1.1)
    plt.savefig('./data/dados_hipotese1/relacao_notas_membros_outros_generos.png')
    plt.close()
    print("Gráfico de relação entre notas e número de membros (Outros Gêneros) salvo.")

    # Criando intervalos de notas
    bins = [0, 2, 4, 6, 8, 10]
    labels = ['0-2', '2-4', '4-6', '6-8', '8-10']

    # Adicionando uma coluna de intervalo de notas nos DataFrames
    anime_populares['nota_intervalo'] = pd.cut(anime_populares['rating'], bins=bins, labels=labels, right=False)
    anime_outros['nota_intervalo'] = pd.cut(anime_outros['rating'], bins=bins, labels=labels, right=False)

    # Calculando o número médio de membros para cada intervalo de nota
    media_membros_populares = anime_populares.groupby('nota_intervalo')['members'].mean()
    media_membros_outros = anime_outros.groupby('nota_intervalo')['members'].mean()

    # Criando o DataFrame para o gráfico de barras
    media_membros_df = pd.DataFrame({
        'Gêneros Populares': media_membros_populares,
        'Outros Gêneros': media_membros_outros
    }).fillna(0)

    # Gráfico de barras para comparação
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    x = range(len(media_membros_df.index))

    plt.bar(x, media_membros_df['Gêneros Populares'], width=bar_width, color='red', label='Gêneros Populares')
    plt.bar([p + bar_width for p in x], media_membros_df['Outros Gêneros'], width=bar_width, color='blue', label='Outros Gêneros')

    plt.title('Número Médio de Membros por Intervalo de Notas')
    plt.xlabel('Intervalo de Notas')
    plt.ylabel('Número Médio de Membros')
    plt.xticks([p + bar_width / 2 for p in x], media_membros_df.index)
    plt.legend()
    plt.savefig('./data/dados_hipotese1/media_membros_por_intervalo_notas.png')
    plt.close()
    print("Gráfico de barras mostrando o número médio de membros por intervalo de notas salvo.")


def processar_anime() -> None:
    """
    Função principal para carregar e processar os dados do arquivo CSV de animes limpos, 
    gerando as análises sobre os gêneros populares e outros gêneros.

    Parameters
    ----------
    None
    
    Returns
    -------
    None
        A função gera gráficos salvos em arquivos e não retorna nenhum valor.
    
    Arquivo Utilizado
    -----------------
    /Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv: Arquivo contendo os dados de animes limpos e filtrados.
    """
    caminho_arquivo = './data/anime_filtrado_limpo.csv'
    
    # Verifica se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return
    
    # Carregar os dados do anime filtrado limpo
    anime_filtrado_limpo = pd.read_csv(caminho_arquivo, encoding='ISO-8859-1', sep=',')
    analisar_generos_populares(anime_filtrado_limpo)


if __name__ == "__main__":
    processar_anime()
