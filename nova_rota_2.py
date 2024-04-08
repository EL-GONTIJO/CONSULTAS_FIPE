import requests
import pandas as pd
from time import sleep


# Função para fazer chamadas à API e retornar os dados
def get_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()  # Lança um erro para respostas de erro
    return response.json()


# Inicializa um DataFrame para armazenar os dados
df_final = pd.DataFrame()

# Base URL
base_url = "https://parallelum.com.br/fipe/api/v1/carros"

# Passo 1: Pegar marcas de carros
marcas_url = f"{base_url}/marcas"
marcas = get_data_from_api(marcas_url)

for marca in marcas:
    marca_id = marca["codigo"]
    print(f"Coletando dados para a marca: {marca['nome']}")

    # Passo 2: Pegar modelos da marca escolhida
    modelos_url = f"{base_url}/marcas/{marca_id}/modelos"
    modelos = get_data_from_api(modelos_url)["modelos"]

    for modelo in modelos:
        modelo_id = modelo["codigo"]

        # Passo 3: Pegar anos do modelo escolhido
        anos_url = f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos"
        anos = get_data_from_api(anos_url)

        for ano in anos:
            ano_codigo = ano["codigo"]

            # Passo 4: Pegar valor para o ano/modelo/marca escolhidos
            valor_url = (
                f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_codigo}"
            )
            valor = get_data_from_api(valor_url)

            # Adiciona os dados coletados ao DataFrame
            df_final = pd.concat([df_final, pd.DataFrame([valor])], ignore_index=True)

            # Uma pequena pausa para não sobrecarregar a API
            sleep(2)

# Salvar os dados em um arquivo Excel
df_final.to_excel("dados_completos_fipe2.xlsx", index=False)

print("Dados coletados e salvos com sucesso no arquivo 'dados_completos_fipe2.xlsx'.")
