import requests
import pandas as pd
from time import sleep
import os


def get_data_from_api(
    url, timeout=7200
):  # Timeout ajustado para 7200 segundos (2 horas)
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Lança um erro para respostas de erro
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None


def save_checkpoint(marca_id, modelo_id, ano_codigo):
    with open("checkpoint.txt", "w") as file:
        file.write(f"{marca_id},{modelo_id},{ano_codigo}")


def load_checkpoint():
    if os.path.exists("checkpoint.txt"):
        with open("checkpoint.txt") as file:
            content = file.read().split(",")
            if len(content) == 3:
                try:
                    return int(content[0]), int(content[1]), content[2]
                except ValueError:
                    print("Formato de checkpoint inválido.")
    else:
        print("Checkpoint não encontrado.")
    return None, None, ""  # Retorna valores padrão


# Inicializa o DataFrame ou lê os dados existentes
if not os.path.exists("dados_completos_fipe2.xlsx"):
    df_final = pd.DataFrame()
else:
    df_final = pd.read_excel("dados_completos_fipe2.xlsx")

# Carrega ou define o checkpoint
checkpoint_marca, checkpoint_modelo, checkpoint_ano = load_checkpoint()

# Base URL
base_url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"

# Inicia a coleta de dados
marcas = get_data_from_api(base_url)
if marcas is None:
    print("Falha ao obter marcas, terminando execução.")
    exit()

for marca in marcas:
    marca_id = int(marca["codigo"])
    if checkpoint_marca is not None and marca_id < checkpoint_marca:
        continue

    modelos_url = f"{base_url}/{marca_id}/modelos"
    modelos = get_data_from_api(modelos_url)
    if modelos and "modelos" in modelos:
        modelos = modelos["modelos"]
    else:
        continue

    for modelo in modelos:
        modelo_id = int(modelo["codigo"])
        if (
            checkpoint_marca == marca_id
            and checkpoint_modelo is not None
            and modelo_id <= checkpoint_modelo
        ):
            continue

        anos_url = f"{base_url}/{marca_id}/modelos/{modelo_id}/anos"
        anos = get_data_from_api(anos_url)
        if not anos:
            continue

        for ano in anos:
            ano_codigo = ano["codigo"]
            if (
                checkpoint_marca == marca_id
                and checkpoint_modelo == modelo_id
                and checkpoint_ano
                and ano_codigo <= checkpoint_ano
            ):
                continue

            valor_url = f"{base_url}/{marca_id}/modelos/{modelo_id}/anos/{ano_codigo}"
            valor = get_data_from_api(valor_url)
            if valor:
                df_final = pd.concat(
                    [df_final, pd.DataFrame([valor])], ignore_index=True
                )
                save_checkpoint(marca_id, modelo_id, ano_codigo)
                sleep(2)

df_final.to_excel("dados_completos_fipe2.xlsx", index=False)
print("Dados coletados e salvos com sucesso no arquivo 'dados_completos_fipe2.xlsx'.")
