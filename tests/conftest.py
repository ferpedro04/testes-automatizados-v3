# Imports
from dotenv import load_dotenv
import os
import pytest 
from datetime import datetime, timedelta

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

produto_erro = {
    "codinterno": "2538685",
    "ean": "7898199100143",
    "descricao": "FORT-MEN 550MG CPR 120UN",
}

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

@pytest.fixture
def retorno_ean_ausente(config):
    produto = produto_erro.copy()
    produto.pop("ean")
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
def retorno_ean_vazio(config):
    produto = produto_erro.copy()
    produto["ean"] = ""
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
def retorno_ean_maior(config):
    produto = produto_erro.copy()
    produto["ean"] = "000000000000000"
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
def retorno_ean_alfanumerico(config):
    produto = produto_erro.copy()
    produto["ean"] = "123ABC"
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
def retorno_descricao_curta(config):
    produto = produto_erro.copy()
    produto["descricao"] = "AB"
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
def retorno_descricao_valida(config):
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
def retorno_codinterno_vazio(config):
    produto = produto_erro.copy()
    produto["codinterno"] = ""
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
def retorno_codinterno_ean_vazios(config):
    produto = produto_erro.copy()
    produto["ean"] = ""
    produto["codinterno"] = ""
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
def retorno_codinterno_ean_invalidos(config):
    produto = produto_erro.copy()
    produto["ean"] = "ABC"
    produto["codinterno"] = "123ABC"
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
def url_token_invalido(config):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/token_invalido"
    return url

@pytest.fixture
def url_token_ausente(config):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/"
    return url

@pytest.fixture
def url_cnpj_invalido(config):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/12345678912345/{config['token']}"
    return url

@pytest.fixture
def url_id_invalido(config):
    url = f"{config['url_base']}/revisao/99999/{config['cnpj']}/{config['token']}"
    return url

@pytest.fixture
def retorno_regime_invalido(config):
    produto = produto_api.copy()
    cmun = config["cmun"]
    crt = config["crt"]
    produto["cMun"] = cmun
    produto["regime"] = "inválido"
    produto["crt"] = crt
    produto["csosn"] = "000"
    produto["ncm"] = "00000000"
    produto["cfop"] = "0000"
    produto["pICMS"] = 0
    produto["cst_pis_saida"] = "00"
    produto["cst_cofins_saida"] = "00"
    return [produto]

@pytest.fixture
def retorno_crt_invalido(config):
    produto = produto_api.copy()
    cmun = config["cmun"]
    regime = config["regime"]
    produto["cMun"] = cmun
    produto["regime"] = regime
    produto["crt"] = 9
    produto["csosn"] = "000"
    produto["ncm"] = "00000000"
    produto["cfop"] = "0000"
    produto["pICMS"] = 0
    produto["cst_pis_saida"] = "00"
    produto["cst_cofins_saida"] = "00"
    return [produto]

@pytest.fixture
def retorno_crt_regime_incompativeis(config):
    produto = produto_api.copy()
    cmun = config["cmun"]
    regime = config["regime"]
    produto["cMun"] = cmun
    produto["regime"] = regime
    produto["crt"] = 3
    produto["csosn"] = "000"
    produto["ncm"] = "00000000"
    produto["cfop"] = "0000"
    produto["pICMS"] = 0
    produto["cst_pis_saida"] = "00"
    produto["cst_cofins_saida"] = "00"
    return [produto]

@pytest.fixture
def retorno_cmun_invalido(config):
    produto = produto_api.copy()
    crt = config["crt"]
    regime = config["regime"]
    produto["cMun"] = 1234567
    produto["regime"] = regime
    produto["crt"] = crt
    produto["csosn"] = "000"
    produto["ncm"] = "00000000"
    produto["cfop"] = "0000"
    produto["pICMS"] = 0
    produto["cst_pis_saida"] = "00"
    produto["cst_cofins_saida"] = "00"
    return [produto]

@pytest.fixture(scope="module")
def cache_respostas():
    return {}

@pytest.fixture
def params_atualizacoes(config):
    date = datetime.now().strftime("%d-%m-%Y")
    params = {
        "regime": config["regime"],
        "cMun": config["cmun"],
        "crt": config["crt"],
        "date": date 
        }
    return params

@pytest.fixture
def params_paginacao(params_atualizacoes):
    params_paginacao = params_atualizacoes.copy()
    params_paginacao["pagina"] = 2
    params_paginacao["limite"] = 5
    return params_paginacao

@pytest.fixture
def params_minimo(params_atualizacoes):
    params_minimo = params_atualizacoes.copy()
    params_minimo["limite"] = 1
    return params_minimo

@pytest.fixture
def params_maximo(params_atualizacoes):
    params_maximo = params_atualizacoes.copy()
    params_maximo["limite"] = 300
    return params_maximo

@pytest.fixture
def params_data_invalida(params_atualizacoes):
    params_data_invalida = params_atualizacoes.copy()
    params_data_invalida["date"] = "2026-10-14"
    return params_data_invalida

@pytest.fixture
def params_data_ausente(params_atualizacoes):
    params_data_ausente = params_atualizacoes.copy()
    params_data_ausente.pop("date")
    return params_data_ausente

@pytest.fixture
def params_data_antiga(params_atualizacoes):
    params_data_antiga = params_atualizacoes.copy()
    params_data_antiga["date"] = (datetime.now() - timedelta(days=8)).strftime("%d-%m-%Y")
    return params_data_antiga

@pytest.fixture
def params_data_superior(params_atualizacoes):
    params_data_superior = params_atualizacoes.copy()
    params_data_superior["date"] = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    return params_data_superior

@pytest.fixture
def params_regime_invalido(params_atualizacoes):
    params_regime_invalido = params_atualizacoes.copy()
    params_regime_invalido["regime"] = "invalido"
    return params_regime_invalido

@pytest.fixture
def params_regime_ausente(params_atualizacoes):
    params_regime_ausente = params_atualizacoes.copy()
    params_regime_ausente.pop("regime")
    return params_regime_ausente

@pytest.fixture
def params_crt_invalido(params_atualizacoes):
    params_crt_invalido = params_atualizacoes.copy()
    params_crt_invalido["crt"] = 86
    return params_crt_invalido

@pytest.fixture
def params_crt_regime_invalidos(params_atualizacoes):
    params_crt_regime_invalidos = params_atualizacoes.copy()
    params_crt_regime_invalidos["crt"] = 3
    return params_crt_regime_invalidos

@pytest.fixture
def params_cmun_invalido(params_atualizacoes):
    params_cmun_invalido = params_atualizacoes.copy()
    params_cmun_invalido["cMun"] = 9999999
    return params_cmun_invalido

@pytest.fixture
def params_pagina_invalida(params_atualizacoes):
    params_pagina_invalida = params_atualizacoes.copy()
    params_pagina_invalida["pagina"] = -1
    return params_pagina_invalida

@pytest.fixture
def params_abaixo_minimo(params_atualizacoes):
    params_abaixo_minimo = params_atualizacoes.copy()
    params_abaixo_minimo["limite"] = -10
    return params_abaixo_minimo

@pytest.fixture
def params_acima_maximo(params_atualizacoes):
    params_acima_maximo = params_atualizacoes.copy()
    params_acima_maximo["limite"] = 350
    return params_acima_maximo

@pytest.fixture
def url_atualizacoes_token_invalido(config):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/token_invalido"
    return url

@pytest.fixture
def url_atualizacoes_cnpj_invalido(config):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/11111111111111/{config['token']}"
    return url