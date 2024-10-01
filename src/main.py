from funcoes import *


data_frame = carregar_dados('./data/dados_completos.csv')
data_frame = data_frame[data_frame['episodes'] != 'Unknown']
data_frame['episodes'] = pd.to_numeric(data_frame['episodes'], errors='coerce')
#data_frame = data_frame[data_frame['episodes'] != np.nan]
'''print(data_frame['episodes'].dtype)
print(data_frame['episodes'].max())'''

