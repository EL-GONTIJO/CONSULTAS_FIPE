import requests
import pandas as pd

# URL da API
url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"

# Faz a chamada à API e armazena a resposta
response = requests.get(url)

# Verifica se a chamada foi bem-sucedida
if response.status_code == 200:
    # Converte a resposta JSON em uma lista de dicionários
    data = response.json()

    # Cria um DataFrame a partir dos dados
    df = pd.DataFrame(data)

    # Define o caminho do arquivo Excel onde os dados serão salvos
    output_file = r"C:\\CONSULTAS_FIPE\\marcas_carros.xlsx"

    # Salva o DataFrame em um arquivo Excel
    df.to_excel(output_file, index=False)

    print(f"Dados salvos com sucesso em: {output_file}")
else:
    print("Falha na chamada da API.")
