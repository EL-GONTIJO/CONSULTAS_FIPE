import requests
import pandas as pd
from time import sleep
import os

# Função para fazer chamadas à API e retornar os dados
def get_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()  # Lança um erro para respostas de erro
    return response.json()

def save_checkpoint(marca_id, modelo_id, ano_codigo):
    with open("checkpoint.txt", "w") as file:
        file.write(f"{marca_id},{modelo_id},{ano_codigo}")

def load_checkpoint():
    if os.path.exists("checkpoint.txt"):
        with open("checkpoint.txt") as file:
            return map(int, file.read().split(','))
    return None, None, None

# Verifica se o arquivo Excel existe; se não, cria um arquivo vazio
if not os.path.exists("dados_completos_fipe2.xlsx"):
    pd.DataFrame().to_excel("dados_completos_fipe2.xlsx", index=False)

# Carrega ou define o checkpoint
checkpoint_marca, checkpoint_modelo, checkpoint_ano = load_checkpoint()

# Base URL
base_url = "https://parallelum.com.br/fipe/api/v1/carros"

marcas_url = f"{base_url}/marcas"
marcas = get_data_from_api(marcas_url)

for marca in marcas:
    marca_id = marca["codigo"]
    
    if checkpoint_marca is not None and marca_id < checkpoint_marca:
        continue
    elif checkpoint_marca is not None and marca_id == checkpoint_marca:
        modelo_checkpoint = checkpoint_modelo
    else:
        modelo_checkpoint = None

    print(f"Coletando dados para a marca: {marca['nome']}")

    modelos_url = f"{base_url}/marcas/{marca_id}/modelos"
    modelos = get_data_from_api(modelos_url)["modelos"]

    for modelo in modelos:
        modelo_id = modelo["codigo"]

        if modelo_checkpoint is not None and modelo_id < modelo_checkpoint:
            continue
        elif modelo_checkpoint is not None and modelo_id == modelo_checkpoint:
            ano_checkpoint = checkpoint_ano
        else:
            ano_checkpoint = None

        anos_url = f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos"
        anos = get_data_from_api(anos_url)

        for ano in anos:
            ano_codigo = ano["codigo"]

            if ano_checkpoint is not None and int(ano_codigo.split('-')[0]) < ano_checkpoint:
                continue

            valor_url = f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_codigo}"
            valor = get_data_from_api(valor_url)

            # Lê o arquivo existente, adiciona a nova linha e salva novamente
            df_final = pd.read_excel("dados_completos_fipe2.xlsx")
            df_final = pd.concat([df_final, pd.DataFrame([valor])], ignore_index=True)
            df_final.to_excel("dados_completos_fipe2.xlsx", index=False)

            save_checkpoint(marca_id, modelo_id, int(ano_codigo.split('-')[0]))

            sleep(2)  # Pequena pausa

print("Dados coletados e salvos com sucesso no arquivo 'dados_completos_fipe2.xlsx'.")
