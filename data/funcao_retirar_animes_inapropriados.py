import csv

def abrir_anime_csv(caminho='anime.csv'):
    try:
        with open(caminho, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            cabecalho = next(reader)  # Lê o cabeçalho
            dados = [row for row in reader]  # Lê todas as linhas
        return cabecalho, dados
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
        return None, None  # Retorna None se houver erro
    except Exception as e:
        print(f"Erro: {e}")
        return None, None

def filtrar_generos(cabecalho, dados):
    # Gêneros que queremos remover
    generos_indesejados = ['hentai', 'yaoi', 'yuri', 'ecchi', 'shota', 'loli', 'harem', 'reverse harem', 'josei']
    
    # Índice da coluna de gêneros
    indice_genero = cabecalho.index('genre')
    
    # Filtra as linhas que não contêm os gêneros indesejados
    dados_filtrados = [row for row in dados if not any(genero in row[indice_genero].lower() for genero in generos_indesejados)]
    
    return dados_filtrados

def salvar_anime_csv(cabecalho, dados, caminho='anime_filtrado.csv'):
    try:
        with open(caminho, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(cabecalho)  # Escreve o cabeçalho
            writer.writerows(dados)      # Escreve os dados filtrados
        print(f"Os dados filtrados foram salvos em '{caminho}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# Exemplo de uso
cabecalho, anime_data = abrir_anime_csv()

if anime_data is not None:  # Verifica se os dados foram carregados corretamente
    # Mostra todos os dados do arquivo completo
    print("Dados completos do Anime:")
    print(cabecalho)  # Mostra o cabeçalho
    for row in anime_data:
        print(row)

    # Filtra os gêneros indesejados
    anime_data_filtrado = filtrar_generos(cabecalho, anime_data)

    # Mostra todos os dados filtrados
    print("\nDados filtrados do Anime (sem gêneros indesejados):")
    print(cabecalho)  # Mostra o cabeçalho
    for row in anime_data_filtrado:
        print(row)

    # Salva os dados filtrados em um novo arquivo CSV
    salvar_anime_csv(cabecalho, anime_data_filtrado)