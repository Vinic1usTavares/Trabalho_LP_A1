import pandas as pd

def limpar_dados(df):
    # Remove linhas onde 'type' está vazio
    df = df[df['type'].notna()]

    # Atualiza 'episodes' para 1 onde 'type' é 'Movie' e 'episodes' é 'unknown'
    df.loc[(df['type'] == 'Movie') & (df['episodes'] == 'unknown'), 'episodes'] = 1

    # Remove linhas onde 'rating', 'genre', 'members' ou 'aired' estão vazios
    df = df[df['rating'].notna()]
    df = df[df['genre'].notna()]
    df = df[df['members'].notna()]
    df = df[df['aired'].notna()]

    return df

# Exemplo de uso
if __name__ == "__main__":
    # Carregar o DataFrame
    df = pd.read_csv('anime_filtrado_datado.csv', encoding='latin1')

    # Limpar os dados
    df_limpinho = limpar_dados(df)

    # Salvar o DataFrame limpo em um novo arquivo
    df_limpinho.to_csv('anime_filtrado_limpo.csv', index=False, encoding='latin1')
