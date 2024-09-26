import pandas as pd
import re

# Função para converter datas para o formato DD/MM/YYYY
def convert_date(date_str):
    match = re.match(r'(\w{3}) (\d{1,2}), (\d{4})', date_str)
    if match:
        month_str, day, year = match.groups()
        month_mapping = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        month = month_mapping.get(month_str)
        return f"{day.zfill(2)}/{month}/{year}"
    return None

# Lê os arquivos CSV com codificações especificadas
anime_filtrado = pd.read_csv('anime_filtrado.csv', encoding='ISO-8859-1')

# Tenta ler o arquivo animes_complemento.csv com delimitador correto
try:
    animes_complemento = pd.read_csv('animes_complemento.csv', encoding='latin1', sep=';', on_bad_lines='skip')  # Adiciona sep=';'
    print("Colunas em animes_complemento:", animes_complemento.columns.tolist())  # Imprime os nomes das colunas
except Exception as e:
    print(f"Erro ao ler animes_complemento.csv: {e}")

# Cria a nova coluna 'aired' no anime_filtrado
anime_filtrado['aired'] = None

# Percorre cada linha do anime_filtrado
for index, row in anime_filtrado.iterrows():
    name = row['name']
    # Busca o nome correspondente no animes_complemento
    matching_row = animes_complemento[animes_complemento['name'] == name]
    if not matching_row.empty:
        aired_value = matching_row['aired'].values[0]  # Pega o primeiro valor da coluna 'aired'
        if pd.notna(aired_value) and isinstance(aired_value, str):
            # Converte a data e atualiza na nova coluna
            first_date = aired_value.split(' to ')[0]  # Pega a primeira data antes do 'to'
            converted_date = convert_date(first_date)
            if converted_date:
                anime_filtrado.at[index, 'aired'] = converted_date

# Salva o novo arquivo CSV
anime_filtrado.to_csv('anime_filtrado_datado.csv', index=False)
