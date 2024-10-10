from funcoes import *

def hipótese_2():
    data_frame = pd.read_csv('./data/data_frame_final.csv',encoding='ISO-8859-1',sep=';')
    data_frame['episodes'] = pd.to_numeric(data_frame['episodes'], errors='coerce')
    data_frame= data_frame[data_frame['episodes'] != np.nan]
    print(data_frame['episodes'].dtype)
    print(data_frame['episodes'].max())
    print(data_frame['episodes'].min())
    labels = ['A','B','C','D','E','F','G','H','I']
    bins_episodes = [0,100,200,300,400,500,600,1000,1500,2000]
    index = ['name','episodes','rating','members']
    selected_data = data_frame[index].copy()
    movies= len(selected_data[selected_data['episodes']== 1])
    print(f"quantidade de filmes: {movies} \n")

    selected_data['episodes'] = pd.cut(selected_data['episodes'] ,bins_episodes, labels=labels)

    # gerando informação para ser explorada:
    print(selected_data.groupby('episodes').count())

    rating_media = selected_data.groupby('episodes')['rating'].mean()
    rating_max = selected_data.groupby('episodes')['rating'].max()
    rating_min = selected_data.groupby('episodes')['rating'].min()
    rating_mediana = selected_data.groupby('episodes')['rating'].median()

     # Gráfico: Episódios x Número de membros
    plt.figure(figsize=(10, 6))
    plt.scatter(data_frame['episodes'], data_frame['members'], alpha=0.5)
    plt.title('Episódios x Número de membros')
    plt.xlabel('Episódios')
    plt.ylabel('Número de membros')
    plt.grid(True)
    plt.savefig('.\data\dados_hipotese2\EpisódiosxNúmero de membros.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos

    # Análise para episódios >= 500
    df_more_episodes = data_frame[(data_frame['episodes'] >= 500) & (data_frame['members'] < 100000)].copy()
    media = df_more_episodes['rating'].mean()
    plt.figure(figsize=(10, 6))
    plt.scatter(df_more_episodes['episodes'], df_more_episodes['members'], alpha=0.5)
    plt.title(f'Episódios(500+) x Número de membros (media:{media})')
    plt.xlabel('Episódios(500+)')
    plt.ylabel('Número de membros')
    plt.grid(True)
    plt.savefig('.\data\dados_hipotese2\Episódios(500+)xNúmero de membros.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos

    # Gráfico: Episódios x Rating
    plt.figure(figsize=(10, 6))
    plt.scatter(data_frame['episodes'], data_frame['rating'], alpha=0.5)
    plt.title('Episódios x rating')
    plt.xlabel('Episódios')
    plt.ylabel('rating')
    plt.grid(True)
    plt.savefig('.\data\dados_hipotese2\Episódiosxrating.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos

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
            f'{bar.get_height()}',  # Valor a ser mostrado
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),  # Posição
            ha='center',  # Alinhamento horizontal
            va='bottom'   # Alinhamento vertical
        )

    plt.title('Quantidade de Animes por Faixa de Episódios')
    plt.xlabel('Faixa de Episódios')
    plt.ylabel('Quantidade de Animes')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig('.\data\dados_hipotese2\Quantidade_x_episodios.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos

  

    '''rating_mediana.plot.bar(x='episodes', y = 'rating', title = 'Média de Rating por intervalo de episódio', color = 'skyblue')
    plt.show()'''

if __name__ == "__main__":
    #processar_anime()
    hipótese_2()
   