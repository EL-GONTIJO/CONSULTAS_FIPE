import requests
import pandas as pd

# Substitua 'seu_arquivo.xlsx' pelo caminho do seu arquivo Excel
df = pd.read_excel("BTG1.xlsx")


def get_marca_id(marca_nome):
    marcas = requests.get("https://parallelum.com.br/fipe/api/v1/carros/marcas").json()
    for marca in marcas:
        if marca["nome"].lower() == marca_nome.lower():
            return marca["codigo"]
    return None


def get_modelo_id(marca_id, modelo_nome):
    modelos = requests.get(
        f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{marca_id}/modelos"
    ).json()["modelos"]
    for modelo in modelos:
        if modelo["nome"].lower() == modelo_nome.lower():
            return modelo["codigo"]
    return None


def get_ano_id(marca_id, modelo_id, ano):
    anos = requests.get(
        f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{marca_id}/modelos/{modelo_id}/anos"
    ).json()
    for ano_opcao in anos:
        if ano_opcao["codigo"].startswith(str(ano)):
            return ano_opcao["codigo"]
    return None


def get_valor_veiculo(marca_id, modelo_id, ano_id):
    valor = requests.get(
        f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_id}"
    ).json()
    return valor["Valor"]


# Exemplo de como chamar as funções para uma linha específica da planilha
marca_nome = "Volkswagen"  # Substitua por df['Marca'][linha] após testar
modelo_nome = "Gol"  # Substitua por df['Modelo'][linha]
ano = 2014  # Substitua por df['Ano'][linha]

marca_id = get_marca_id(marca_nome)
modelo_id = get_modelo_id(marca_id, modelo_nome)
ano_id = get_ano_id(marca_id, modelo_id, ano)

if marca_id and modelo_id and ano_id:
    valor_veiculo = get_valor_veiculo(marca_id, modelo_id, ano_id)
    print(f"O valor do veículo {modelo_nome} {ano} é: {valor_veiculo}")
else:
    print("Não foi possível encontrar os dados solicitados.")
