import requests
import pandas as pd

# Substitua 'caminho_para_sua_planilha.xlsx' pelo caminho real da sua planilha Excel
caminho_planilha = r"C:\\CONSULTAS_FIPE\\BTG1.xlsx"

# Primeira chamada à API para obter todas as marcas
url_marcas = 'https://parallelum.com.br/fipe/api/v1/carros/marcas'
response_marcas = requests.get(url_marcas)
marcas = response_marcas.json()

# Lendo a planilha Excel
df = pd.read_excel(caminho_planilha)

# Iterar sobre cada linha da planilha
for index, row in df.iterrows():
    marca_carro = row[
        "marca_veiculo"
    ]  # Substitua 'Marca' pelo nome real da coluna na sua planilha
    id_marca = None

    # Encontrar o ID da marca baseado no nome
    for marca in marcas:
        if marca['nome'].lower() == marca_carro.lower():
            id_marca = marca['codigo']
            break

    if id_marca:
        # Fazer a chamada à API com o ID da marca
        url_modelos = f'https://parallelum.com.br/fipe/api/v1/carros/marcas/{id_marca}/modelos'
        response_modelos = requests.get(url_modelos)
        modelos = response_modelos.json()

        # Aqui você pode processar os modelos e fazer o que precisar com os dados
        print(modelos)  # Exemplo: Imprimir os modelos
    else:
        print(f'Marca "{marca_carro}" não encontrada.')
