import requests
import pandas as pd
from time import sleep
import os


# Função para fazer chamadas à API e retornar os dados
def get_data_from_api(url, timeout=7200):  # Timeout ajustado para 7200 segundos (2 horas)
    response = requests.get(url)
    response.raise_for_status()  # Lança um erro para respostas de erro
    return response.json()


def save_checkpoint(marca_id, modelo_id, ano_codigo):
    with open("checkpoint.txt", "w") as file:
        file.write(f"{marca_id},{modelo_id},{ano_codigo}")


def load_checkpoint():
    if os.path.exists("checkpoint.txt"):
        with open("checkpoint.txt") as file:
            content = file.read().split(",")
            if len(content) == 3:
                marca_id, modelo_id, ano_codigo = content
                return int(marca_id), int(modelo_id), ano_codigo
            else:
                return (
                    None,
                    None,
                    "",
                )  # Retorna valores padrão se o arquivo não estiver no formato esperado
    return None, None, ""  # Retorna valores padrão se o arquivo não existir


# Inicializa o DataFrame ou lê os dados existentes
if not os.path.exists("dados_completos_fipe2.xlsx"):
    df_final = pd.DataFrame()
else:
    df_final = pd.read_excel("dados_completos_fipe2.xlsx")

# Carrega ou define o checkpoint
checkpoint_marca, checkpoint_modelo, checkpoint_ano = load_checkpoint()

# Base URL
base_url = "https://parallelum.com.br/fipe/api/v1/carros"

# Inicia a coleta de dados
marcas_url = f"{base_url}/marcas"
marcas = get_data_from_api(marcas_url)

for marca in marcas:
    marca_id = int(marca["codigo"])

    # Pula marcas já processadas
    if checkpoint_marca is not None and marca_id < checkpoint_marca:
        continue

    print(f"Coletando dados para a marca: {marca['nome']}")

    modelos_url = f"{base_url}/marcas/{marca_id}/modelos"
    modelos = get_data_from_api(modelos_url)["modelos"]

    for modelo in modelos:
        modelo_id = int(modelo["codigo"])

        # Pula modelos já processados da marca atual
        if (
            checkpoint_marca == marca_id
            and checkpoint_modelo is not None
            and modelo_id <= checkpoint_modelo
        ):
            continue

        anos_url = f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos"
        anos = get_data_from_api(anos_url)

        for ano in anos:
            ano_codigo = ano["codigo"]

            # Pula anos já processados do modelo atual
            if (
                checkpoint_marca == marca_id
                and checkpoint_modelo == modelo_id
                and ano_codigo <= checkpoint_ano
            ):
                continue

            valor_url = (
                f"{base_url}/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_codigo}"
            )
            valor = get_data_from_api(valor_url)

            # Adiciona os dados coletados ao DataFrame
            df_final = pd.concat([df_final, pd.DataFrame([valor])], ignore_index=True)

            # Salva o checkpoint após cada registro
            save_checkpoint(marca_id, modelo_id, ano_codigo)

            sleep(2)  # Pequena pausa

# Salva os dados finais em um arquivo Excel
df_final.to_excel("dados_completos_fipe2.xlsx", index=False)

print("Dados coletados e salvos com sucesso no arquivo 'dados_completos_fipe2.xlsx'.")
