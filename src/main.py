from data_functions import *



data_frame_principal = carregar_dados('./data/anime.csv')
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
print(data_frame_principal.columns)

#data_frame_completo = pd.merge(data_frame_principal,data_frame_complementar, on='episodes',how='outer')
#print(data_frame_completo.head)