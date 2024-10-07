from funcoes import *
import matplotlib.pyplot as plt


data_frame = carregar_dados('./data/dados_completos.csv')
data_frame = data_frame[data_frame['episodes'] != 'Unknown']
data_frame['episodes'] = pd.to_numeric(data_frame['episodes'], errors='coerce')
data_frame = data_frame[data_frame['episodes'] != np.nan]
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

'''print(rating_max)
print(rating_min)
print(rating_media)
#print(rating_moda)
print(rating_mediana)
'''


