import requests
import pandas as pd


# Função para fazer chamadas à API e retornar os dados
def get_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()  # Lança um erro para respostas de erro
    return response.json()


# Base URL
base_url = "https://parallelum.com.br/fipe/api/v1/carros"

# Passo 1: Pegar marcas de carros
marcas_url = f"{base_url}/marcas"
marcas = get_data_from_api(marcas_url)

# Para este exemplo, vamos pegar apenas a primeira marca (deve ser adaptado)
marca_id = marcas[0]["codigo"]

# Passo 2: Pegar modelos da marca escolhida
modelos_url = f"{base_url}/marcas/{marca_id}/modelos"
modelos = get_data_from_api(modelos_url)["modelos"]

# Pegar apenas o primeiro modelo (deve ser adaptado)
modelo_id = modelos[0]["codigo"]

# Passo 3: Pegar anos do modelo escolhido
anos_url = f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos"
anos = get_data_from_api(anos_url)

# Pegar apenas o primeiro ano (deve ser adaptado)
ano_codigo = anos[0]["codigo"]

# Passo 4: Pegar valor para o ano/modelo/marca escolhidos
valor_url = f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_codigo}"
valor = get_data_from_api(valor_url)

# Criar um DataFrame com os dados coletados
df = pd.DataFrame([valor])

# Salvar os dados em um arquivo Excel
df.to_excel("dados_fipe.xlsx", index=False)

print("Dados salvos com sucesso no arquivo 'dados_fipe.xlsx'.")
