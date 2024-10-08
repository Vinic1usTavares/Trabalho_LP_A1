from funcoes import *
import matplotlib.pyplot as plt

def hipótese_2():
    data_frame = carregar_dados('./data/dados_completos.csv')
    print(data_frame['episodes'].dtype)
    print(data_frame['episodes'].max())
    print(data_frame['episodes'].min())
    labels = ['A','B','C','D','E','F','G','H','I','J','K','L']
    bins_episodes = [0,100,200,300,400,500,600,700,800,1000,1200,1500,2000]
    index = ['name','episodes','rating','members']
    selected_data = data_frame[index].copy()

    selected_data['episodes'] = pd.cut(selected_data['episodes'] ,bins_episodes, labels=labels)

    rating_media = selected_data.groupby('episodes')['rating'].mean()
    rating_max = selected_data.groupby('episodes')['rating'].max()
    rating_min = selected_data.groupby('episodes')['rating'].min()
    #rating_moda = selected_data.groupby('episodes')['rating'].mode()
    rating_mediana = selected_data.groupby('episodes')['rating'].median()

    rating_mediana.plot.bar(x='episodes', y = 'rating', title = 'Média de Rating por intervalo de episódio', color = 'skyblue')
    plt.show()

def gerar_df_limpo():
    data_frame_principal = carregar_dados('./data/anime_filtrado_limpo.csv')
    data_frame_complementar = carregar_dados('./data/animes_complemento.csv')
    data_frame_principal = limpar_dados(data_frame_principal)
    data_frame_complementar = limpar_dados(data_frame_complementar)

    novos_index ={
    'anime_id':'uid',
    'name':'title',
    'rating':'score'
    }
    data_frame_principal = trocar_index(data_frame_principal, novos_index)
    data_frame_complementar = selecionar_colunas(data_frame_complementar, ['uid','title','genre','episodes','score','members'])
    data_frame_complementar = pd.merge(data_frame_principal,data_frame_complementar, on='episodes',how='outer')
    data_frame_complementar = data_frame_complementar[data_frame_complementar['episodes'] != 'Unknown']
    data_frame_complementar['episodes'] = pd.to_numeric(data_frame_complementar['episodes'], errors='coerce')
    data_frame_complementar = data_frame_complementar[data_frame_complementar['episodes'] != np.nan]

    return data_frame_complementar

df = carregar_dados('./data/anime.csv')
print(df['type'].loc['Unknown'])