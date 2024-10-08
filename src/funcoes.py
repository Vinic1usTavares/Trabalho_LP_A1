import pandas as pd
import matplotlib.pyplot as plt
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
    anime_df = pd.read_csv(arquivo_csv, encoding='ISO-8859-1', sep=';')
     
    # Extrair o ano da coluna 'aired'
    anime_df['ano'] = anime_df['aired'].apply(extrair_ano)
    
    # Converter as colunas relevantes para tipos numéricos
    anime_df['ano'] = pd.to_numeric(anime_df['ano'], errors='coerce')
    anime_df['rating'] = pd.to_numeric(anime_df['rating'], errors='coerce')
    anime_df['members'] = pd.to_numeric(anime_df['members'], errors='coerce')
    
    # Calcular correlação entre ano e número de membros
    correlacao_membros = anime_df['ano'].corr(anime_df['members'])
    print(f"Correlação entre ano de lançamento e número de membros: {correlacao_membros}")
    
    # Calcular correlação entre ano e nota (rating)
    correlacao_rating = anime_df['ano'].corr(anime_df['rating'])
    print(f"Correlação entre ano de lançamento e nota (rating): {correlacao_rating}")
    
    # Gráfico: Ano de lançamento x Número de membros
    plt.figure(figsize=(10, 6))
    plt.scatter(anime_df['ano'], anime_df['members'], alpha=0.5)
    plt.title('Ano de lançamento vs. Número de membros')
    plt.xlabel('Ano de lançamento')
    plt.ylabel('Número de membros')
    plt.grid(True)
    plt.savefig('ano_vs_membros.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos
    
    # Gráfico: Ano de lançamento x Nota (rating)
    plt.figure(figsize=(10, 6))
    plt.scatter(anime_df['ano'], anime_df['rating'], alpha=0.5, color='orange')
    plt.title('Ano de lançamento vs. Nota (rating)')
    plt.xlabel('Ano de lançamento')
    plt.ylabel('Nota (rating)')
    plt.grid(True)
    plt.savefig('ano_vs_rating.png')  # Salvar o gráfico
    plt.close()  # Fechar a figura para evitar conflitos

    # Retornar o nome dos arquivos gerados
    return 'ano_vs_membros.png', 'ano_vs_rating.png'

# Executar a função
if __name__ == "__main__":
    arquivo = '/Python/projeto/Trabalho_LP_A1/data/anime_filtrado_limpo.csv'
    analisar_hipotese(arquivo)
