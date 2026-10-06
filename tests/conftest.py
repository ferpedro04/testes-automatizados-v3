# Imports
from dotenv import load_dotenv
import os
import pytest 

# Dados de teste
produto_api = {
    "codinterno": "74663",
    "ean": "7898021390155",
    "descricao": "Cond Kamura Mocoto 1kg",
}

produtos_multiplos_testes = [
{ 
    "codinterno": "2652857", 
    "ean": "1789102210037", 
    "descricao": "Deterlimpol Natcrist 24x500", 
},
{ 
    "codinterno": "634092", 
    "ean": "7896013556312", 
    "descricao": "Creme de Tratamento Novex Iluminadora 300 gr", 
},
{ 
    "codinterno": "1789735", 
    "ean": "7898232553073", 
    "descricao": "Funda P/hernia Inguinal 80cm Dupla", 
},
{ 
    "codinterno": "3003893", 
    "ean": "7898157729270", 
    "descricao": "Agulha Sutura Gr 1 14x80 pct c/12 Procare", 
},
{ 
    "codinterno": "2823127", 
    "ean": "7896007549436", 
    "descricao": "Kit Huggies Classic Cr Assadura 3un", 
},
]

# Carregamento da Env
load_dotenv()

url_base = os.getenv("URL_BASE")
id_parceiro = int(os.getenv("ID_PARCEIRO"))
cnpj = os.getenv("CNPJ")
token = os.getenv("TOKEN")
cmun = os.getenv("CMUN")
regime = os.getenv("REGIME")
crt = int(os.getenv("CRT"))

# Criação das Fixtures
@pytest.fixture
def config():
    return {
        "url_base": url_base,
        "id_parceiro": id_parceiro,
        "cnpj": cnpj,
        "token": token,
        "cmun": cmun,
        "regime": regime,
        "crt": crt
    }

@pytest.fixture
def retorno_produto_api(config):
    produto = produto_api.copy()
    cmun = config["cmun"]
    regime = config["regime"]
    crt = config["crt"]
    produto["cMun"] = cmun
    produto["regime"] = regime
    produto["crt"] = crt
    produto["csosn"] = "000"
    produto["ncm"] = "00000000"
    produto["cfop"] = "0000"
    produto["pICMS"] = 0
    produto["cst_pis_saida"] = "00"
    produto["cst_cofins_saida"] = "00"
    return [produto]

@pytest.fixture
def retorno_produtos_multiplos_testes(config):
    produtos_copiados = []
    cmun = config["cmun"] 
    regime = config["regime"] 
    crt = config["crt"] 
    for produto in produtos_multiplos_testes:
        produto_copiado = produto.copy()
        produto_copiado["cMun"] = cmun 
        produto_copiado["regime"] = regime 
        produto_copiado["crt"] = crt 
        produto_copiado["csosn"] = "000" 
        produto_copiado["ncm"] = "00000000" 
        produto_copiado["cfop"] = "0000" 
        produto_copiado["pICMS"] = 0 
        produto_copiado["cst_pis_saida"] = "00" 
        produto_copiado["cst_cofins_saida"] = "00"
        produtos_copiados.append(produto_copiado)
    return(produtos_copiados)
