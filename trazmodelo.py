import requests
import pandas as pd

# URL da API
url = "https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos"

# Faz a chamada à API e armazena a resposta
response = requests.get(url)

# Verifica se a chamada foi bem-sucedida
if response.status_code == 200:
    # Converte a resposta JSON em uma lista de dicionários
    data = response.json()

    # Verifica a estrutura do JSON e extrai a parte relevante, se necessário
    # Supondo que a estrutura do JSON seja {'modelos': [...]}, 'modelos' é a chave que contém a lista de modelos
    modelos = data.get("modelos") if "modelos" in data else data

    # Cria um DataFrame a partir dos dados
    df = pd.DataFrame(modelos)

    # Define o caminho do arquivo Excel onde os dados serão salvos
    output_file = r"C:\\CONSULTAS_FIPE\\modelos_carros.xlsx"

    # Salva o DataFrame em um arquivo Excel
    df.to_excel(output_file, index=False)

    print(f"Dados salvos com sucesso em: {output_file}")
else:
    print(f"Falha na chamada da API: {response.status_code}")
