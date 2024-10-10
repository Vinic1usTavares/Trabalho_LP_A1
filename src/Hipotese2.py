import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def hipotese2():
    # Abrindo o data frame
    data_frame = pd.read_csv('./data/anime_filtrado_limpo.csv',encoding='ISO-8859-1',sep=',')

    # Convertendo o tipo da coluna episódios para numérico
    data_frame['episodes'] = pd.to_numeric(data_frame['episodes'], errors='coerce')
    data_frame= data_frame[data_frame['episodes'] != np.nan]

    # Informações básicas do Data Frame
    print(f"valor máximo da coluna de episódios: {data_frame['episodes'].max()}")
    print(f"valor mínimo da coluna de episódios: {data_frame['episodes'].min()}")

    # Discretizando os valores 

    labels = ['A','B','C','D','E','F','G','H','I']
    bins_episodes = [0,100,200,300,400,500,600,1000,1500,2000]
    index = ['name','episodes','rating','members', 'type']
    selected_data = data_frame[index].copy()

    movies= len(selected_data[selected_data['type'] == "Movie"])
    print(f"quantidade de filmes: {movies} \n")

    selected_data['episodes'] = pd.cut(selected_data['episodes'] ,bins_episodes, labels=labels)


    # Gerando informação para ser explorada:

    print(selected_data.groupby('episodes').count())

    

    # Gera informação para analizar a relação entre a quantidade de episódios de uma obra e o número de membros

    # Gráfico: Episódios x Número de membros
    plt.figure(figsize=(10, 6))
    plt.scatter(data_frame['episodes'], data_frame['members'], alpha=0.5)
    plt.title('Episódios x Número de membros')
    plt.xlabel('Episódios')
    plt.ylabel('Número de membros')
    plt.grid(True)
    plt.savefig('.\data\dados_hipotese2\EpisódiosxNúmero de membros.png') # Salvar o gráfico
    plt.close() # Fechar a figura para evitar conflitos


    # Análise detalhada de episódios X membros para episódios >= 500
    df_more_episodes = data_frame[(data_frame['episodes'] >= 500) & (data_frame['members'] < 100000)].copy() # members <100 000 para não contabilizar "outliners"
    media = round(df_more_episodes['rating'].mean(), 2) # média de rating dos episódios com valor >= 500
    mediana = round(df_more_episodes['rating'].median(), 2) # mediana de rating dos episódios com valor >= 500

    # Geração do gráfico
    plt.figure(figsize=(10, 6))
    plt.scatter(df_more_episodes['episodes'], df_more_episodes['members'], alpha=0.5)
    plt.title(f'Episódios(500+) x Número de membros (media:{media}, mediana: {mediana})')
    plt.xlabel('Episódios(500+)')
    plt.ylabel('Número de membros')
    plt.grid(True)
    plt.savefig('.\data\dados_hipotese2\Episódios(500+)xNúmero de membros.png') # Salvar o gráfico
    plt.close() # Fechar a figura para evitar conflitos

    
    # Gera informação para análise da relação entre número de episódios e rating de uma obra

    # Gráfico: Episódios x Rating
    plt.figure(figsize=(10, 6))
    plt.scatter(data_frame['episodes'], data_frame['rating'], alpha=0.5)
    plt.title('Episódios x rating')
    plt.xlabel('Episódios')
    plt.ylabel('rating')
    plt.grid(True)
    plt.savefig('.\data\dados_hipotese2\Episódiosxrating.png') # Salvar o gráfico
    plt.close() # Fechar a figura para evitar conflitos

    

    # Análise para episódios < 125

    df_less_episodes = data_frame[data_frame['episodes'] <= 125].copy() # Seleção dos episódios com valor menor ou igual a 125
    media = round(df_less_episodes['rating'].mean(), 2) # média dos ratings
    mediana = round(df_less_episodes['rating'].median(), 2) # mediana dos ratings

    # Geração do Gráfico
    plt.figure(figsize=(10, 6))
    plt.scatter(df_less_episodes['episodes'], df_less_episodes['rating'], alpha=0.5)
    plt.title(f'Episódios(125-) x Rating (media:{media}, mediana: {mediana})')
    plt.xlabel('Episódios(125-)')
    plt.ylabel('rating')
    plt.grid(True)
    plt.savefig('.\data\dados_hipotese2\Episódios(125-)xrating') # Salvar o gráfico
    plt.close() # Fechar a figura para evitar conflitos

    

    # Gráfico: Distribuição de animes x episódios

    index = ['name','episodes']
    selected_data2 = data_frame[index].copy()

    # Discretizando valores
    labels = ['0-20','101-200','201-300','301-400','401-200']
    bins_episodes = [0,20,50,100,400,2000]
    selected_data2['episodes_range'] = pd.cut(selected_data2['episodes'] , bins=bins_episodes, right=False)

    # Contando a quantidade de animes em cada faixa
    counts = selected_data2['episodes_range'].value_counts().sort_index()

    # Plotando o gráfico de barras
    plt.figure(figsize=(10, 6))
    bars = counts.plot(kind='bar', color='skyblue')

    # Adicionando anotações com a quantidade em cada barra
    for bar in bars.patches:
        bars.annotate(
        f'{bar.get_height()}', # Valor a ser mostrado
        (bar.get_x() + bar.get_width() / 2, bar.get_height()),# Posição
        ha='center',# Alinhamento horizontal
        va='bottom'  # Alinhamento vertical
        )

    # Gera dados para analizar a quantidade de obras por faixa de episódios
    plt.title('Quantidade de Animes por Faixa de Episódios')
    plt.xlabel('Faixa de Episódios')
    plt.ylabel('Quantidade de Animes')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig('.\data\dados_hipotese2\Quantidade_x_episodios.png') # Salvar o gráfico
    plt.close() # Fechar a figura para evitar conflitos

if __name__ == "__main__":
    hipotese2()
