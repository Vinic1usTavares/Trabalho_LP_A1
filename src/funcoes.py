import pandas as pd
import os
import matplotlib.pyplot as plt

#Hipotese 1
# Função para analisar a hipótese sobre os gêneros populares
import pandas as pd
import matplotlib.pyplot as plt
import os

def analisar_generos_populares(anime_data):
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
    plt.scatter(anime_populares['rating'], anime_populares['members'], color='blue', alpha=0.7)  # Invertido
    plt.title('Relação entre Nota e Número de Membros para Animes de Gêneros Populares')
    plt.xlabel('Nota (0-10)')  # Ajustar para a faixa correta
    plt.ylabel('Número de Membros')
    plt.xlim(0, 10)  # Ajusta o limite do eixo x para a faixa de notas
    plt.ylim(0, anime_data['members'].max() * 1.1)  # Ajusta o limite do eixo y
    plt.savefig('/Python/projeto/Trabalho_LP_A1/data/relacao_notas_membros_generos_populares.png')
    plt.close()  # Fecha a figura para liberar memória
    print("Gráfico de relação entre notas e número de membros (Gêneros Populares) salvo.")

    # Gráfico para Outros Gêneros
    plt.figure(figsize=(12, 8))
    plt.scatter(anime_outros['rating'], anime_outros['members'], color='gray', alpha=0.5)  # Invertido
    plt.title('Relação entre Nota e Número de Membros para Animes de Outros Gêneros')
    plt.xlabel('Nota (0-10)')  # Ajustar para a faixa correta
    plt.ylabel('Número de Membros')
    plt.xlim(0, 10)  # Ajusta o limite do eixo x para a faixa de notas
    plt.ylim(0, anime_data['members'].max() * 1.1)  # Ajusta o limite do eixo y
    plt.savefig('/Python/projeto/Trabalho_LP_A1/data/relacao_notas_membros_outros_generos.png')
    plt.close()  # Fecha a figura para liberar memória
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
    plt.xticks([p + bar_width / 2 for p in x], media_membros_df.index)  # Ajustar os rótulos do eixo x
    plt.legend()
    plt.savefig('/Python/projeto/Trabalho_LP_A1/data/media_membros_por_intervalo_notas.png')
    plt.close()  # Fecha a figura para liberar memória
    print("Gráfico de barras mostrando o número médio de membros por intervalo de notas salvo.")

# Função principal para processar a análise
def processar_anime():
    caminho_arquivo = '/Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv'
    
    # Verifica se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return
    
    # Carregar os dados do anime filtrado limpo
    anime_filtrado_limpo = pd.read_csv(caminho_arquivo, encoding='ISO-8859-1', sep=',')
    analisar_generos_populares(anime_filtrado_limpo)

if __name__ == "__main__":
    processar_anime()













#Hipotese 3

import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Função para extrair o ano do campo 'aired' no formato DD/MM/YYYY
def extrair_ano(data_str):
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y").year
    except (ValueError, TypeError):
        return None

# Função para analisar a correlação e gerar gráficos
def analisar_hipotese(arquivo_csv):
    # Carregar os dados do arquivo
    anime_df = pd.read_csv(arquivo_csv, encoding='ISO-8859-1', sep=',')
     
    # Extrair o ano da coluna 'aired'
    anime_df['ano'] = anime_df['aired'].apply(extrair_ano)
    
    # Converter as colunas relevantes para tipos numéricos
    anime_df['ano'] = pd.to_numeric(anime_df['ano'], errors='coerce')
    anime_df['rating'] = pd.to_numeric(anime_df['rating'], errors='coerce')
    anime_df['members'] = pd.to_numeric(anime_df['members'], errors='coerce')

    # Definir ano atual e ano limite para animes recentes (10 anos)
    ano_limite = 2010
    ano_maximo = 2017  # Definido como a data limite do dataset

    # Gráfico combinado
    plt.figure(figsize=(12, 6))

    # Animes Recentes
    animes_recentes = anime_df[anime_df['ano'] >= ano_limite]
    plt.scatter(animes_recentes['ano'], animes_recentes['members'], 
                alpha=0.5, color='blue', label='Animes Recentes (2010-2017)')

    # Animes Não Recentes
    animes_nao_recentes = anime_df[anime_df['ano'] < ano_limite]
    plt.scatter(animes_nao_recentes['ano'], animes_nao_recentes['members'], 
                alpha=0.5, color='gray', label='Animes Não Recentes (Antes de 2010)')
    
    # Linha vertical em x=2010
    plt.axvline(x=ano_limite, color='red', linestyle='--', label='Limiar de 2010')

    # Calcular a média do número de membros por ano
    media_membros_por_ano = anime_df.groupby('ano')['members'].mean().dropna()

    # Adicionar linha de tendência
    plt.plot(media_membros_por_ano.index, media_membros_por_ano, color='yellow', label='Média de Membros por Ano')  # Cor da linha de tendência alterada

    plt.title('Ano de Lançamento vs. Número de Membros (Até 2017)')
    plt.xlabel('Ano de Lançamento')
    plt.ylabel('Número de Membros')
    plt.grid(True)
    plt.xlim(anime_df['ano'].min(), ano_maximo)  # Ajustar limites do eixo x
    plt.ylim(0, anime_df['members'].max() * 1.1)  # Ajusta o limite do eixo y
    plt.legend()  # Adicionar legenda
    plt.savefig('/Python/projeto/Trabalho_LP_A1/data/ano_vs_membros_combinado.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos

    # Gráfico de barras para membros médios por intervalo
    plt.figure(figsize=(12, 6))
    bins = np.arange(1940, 2020, 10)  # Intervalos de 10 anos, começando em 1940
    labels = [f'{i}-{i+10}' for i in bins[:-1]]  # Criar rótulos para os intervalos
    
    # Adicionar coluna de intervalo
    anime_df['intervalo'] = pd.cut(anime_df['ano'], bins=bins, right=False, labels=labels)

    # Calcular o número médio de membros por intervalo
    media_membros = anime_df.groupby('intervalo')['members'].mean()

    # Criar gráfico de barras
    media_membros.plot(kind='bar', color='cyan')
    plt.title('Número Médio de Membros por Intervalo de Lançamento')
    plt.xlabel('Intervalo de Lançamento')
    plt.ylabel('Número Médio de Membros')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.savefig('/Python/projeto/Trabalho_LP_A1/data/membros_medio_por_intervalo.png')  # Salvar gráfico
    plt.close()  # Fechar a figura para evitar conflitos

    # Retornar os nomes dos arquivos gerados
    return (
        '/Python/projeto/Trabalho_LP_A1/data/ano_vs_membros_combinado.png',
        '/Python/projeto/Trabalho_LP_A1/data/membros_medio_por_intervalo.png'
    )

# Executar a função
if __name__ == "__main__":
    arquivo = '/Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv'
    analisar_hipotese(arquivo)
