# Imports
import requests
import pytest
import math


# Bloco 1 - Teste de sucesso HTTP 200, Erro 0 e Mensagem
def test_atualizacoes_status_200(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_atualizacoes_200" not in cache_respostas:
        print("FAZENDO REQUEST - GET STATUS 200")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_atualizacoes_200"] = response
    response = cache_respostas["cache_atualizacoes_200"] 
    assert response.status_code == 200

def test_erro_200(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_atualizacoes_200" not in cache_respostas:
        print("FAZENDO REQUEST - GET STATUS 200")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_atualizacoes_200"] = response
    response = cache_respostas["cache_atualizacoes_200"] 
    dados = response.json()
    assert dados["erro"] == 0

def test_mensagem_200(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_atualizacoes_200" not in cache_respostas:
        print("FAZENDO REQUEST - GET STATUS 200")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_atualizacoes_200"] = response
    response = cache_respostas["cache_atualizacoes_200"] 
    dados = response.json()
    assert dados["mensagem"] in ("sucesso", "Nenhuma atualizacao encontrada")

# Bloco 2 - Validação da estrutura de paginação
def test_pagina_atual(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_atual" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_pagina_atual"] = response
    response = cache_respostas["cache_pagina_atual"] 
    dados = response.json()
    assert dados["paginacao"]["pagina_atual"] == 1

def test_limite_por_pagina(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_atual" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_pagina_atual"] = response
    response = cache_respostas["cache_pagina_atual"] 
    dados = response.json()
    assert dados["paginacao"]["limite_por_pagina"] == 300

def test_total_registros(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_atual" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_pagina_atual"] = response
    response = cache_respostas["cache_pagina_atual"] 
    dados = response.json()
    itens = dados.get("itens") or []
    assert len(itens)== dados["paginacao"]["total_registros"]

def test_total_paginas(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_atual" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_pagina_atual"] = response
    response = cache_respostas["cache_pagina_atual"] 
    dados = response.json()
    total_registros = dados["paginacao"]["total_registros"]
    limite = dados["paginacao"]["limite_por_pagina"]
    paginas_esperadas = math.ceil(total_registros / limite)
    assert dados["paginacao"]["total_paginas"] == paginas_esperadas

def test_proxima_pagina(config, params_atualizacoes, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_atual" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS")
        response = requests.get(url, params=params_atualizacoes)
        cache_respostas["cache_pagina_atual"] = response
    response = cache_respostas["cache_pagina_atual"] 
    dados = response.json()
    if dados["paginacao"]["pagina_atual"] < dados["paginacao"]["total_paginas"]:
        proxima_pagina = dados["paginacao"]["pagina_atual"] + 1
        assert dados["paginacao"]["proxima_pagina"] == proxima_pagina
    else:
        assert dados["paginacao"]["proxima_pagina"] is None 

# Bloco 3 - Validação da paginação com parâmetros explícitos
def test_pagina_2(config, params_paginacao, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_paginacao_2" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS NÚMERADAS")
        response = requests.get(url, params=params_paginacao)
        cache_respostas["cache_paginacao_2"] = response
    response = cache_respostas["cache_paginacao_2"] 
    dados = response.json()
    if dados["mensagem"] == "pagina inválida. Esta consulta não tem atualizações; use pagina 1.":
        pytest.skip("Massa de dados insuficiente para validar a segunda página")
    assert dados["paginacao"]["pagina_atual"] == params_paginacao["pagina"]

def test_limite_paginacao(config, params_paginacao, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_paginacao_2" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS NÚMERADAS")
        response = requests.get(url, params=params_paginacao)
        cache_respostas["cache_paginacao_2"] = response
    response = cache_respostas["cache_paginacao_2"] 
    dados = response.json()
    if dados["mensagem"] == "pagina inválida. Esta consulta não tem atualizações; use pagina 1.":
        pytest.skip("Massa de dados insuficiente para validar a segunda página")
    assert dados["paginacao"]["limite_por_pagina"] == params_paginacao["limite"]

def test_quantidade_itens_paginacao(config, params_paginacao, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_paginacao_2" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS NÚMERADAS")
        response = requests.get(url, params=params_paginacao)
        cache_respostas["cache_paginacao_2"] = response
    response = cache_respostas["cache_paginacao_2"] 
    dados = response.json()
    if dados["mensagem"] == "pagina inválida. Esta consulta não tem atualizações; use pagina 1.":
        pytest.skip("Massa de dados insuficiente para validar a segunda página")
    pagina_atual = dados["paginacao"]["pagina_atual"]
    total_registros = dados["paginacao"]["total_registros"]
    limite = params_paginacao["limite"]
    registros_anteriores = (pagina_atual - 1) * limite
    registros_restantes = total_registros- registros_anteriores
    itens_esperados = min(registros_restantes, limite)
    itens = dados.get("itens") or []
    assert len(itens) == itens_esperados

def test_navegacao_proxima_pagina(config, params_paginacao, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_paginacao_2" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINAS NÚMERADAS")
        response = requests.get(url, params=params_paginacao)
        cache_respostas["cache_paginacao_2"] = response
    response = cache_respostas["cache_paginacao_2"] 
    dados = response.json()
    if dados["mensagem"] == "pagina inválida. Esta consulta não tem atualizações; use pagina 1.":
            pytest.skip("Massa de dados insuficiente para validar a segunda página")
    proxima_pagina = dados["paginacao"]["proxima_pagina"]
    print(dados["paginacao"])
    if dados["paginacao"]["total_paginas"] <= params_paginacao["pagina"]:
        pytest.skip("Massa de dados insuficiente para validar a navegação entre páginas")
    params_proxima = params_paginacao.copy()
    params_proxima["pagina"] = proxima_pagina
    if "cache_paginacao_3" not in cache_respostas:
        response_proxima = requests.get(url, params=params_proxima)
        cache_respostas["cache_paginacao_3"] = response_proxima
    response_proxima = cache_respostas["cache_paginacao_3"]
    dados_proxima = response_proxima.json()
    assert dados_proxima["paginacao"]["pagina_atual"] == proxima_pagina

# Bloco 4 - Validação dos limites mínimo e máximo de paginação
def test_limite_minimo(config, params_minimo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_limite_minimo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE MINIMO")
        response = requests.get(url, params=params_minimo)
        cache_respostas["cache_limite_minimo"] = response
    response = cache_respostas["cache_limite_minimo"] 
    dados = response.json()
    assert dados["paginacao"]["limite_por_pagina"] == params_minimo["limite"]

def test_limite_maximo(config, params_maximo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_limite_maximo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE MAXIMO")
        response = requests.get(url, params=params_maximo)
        cache_respostas["cache_limite_maximo"] = response
    response = cache_respostas["cache_limite_maximo"] 
    dados = response.json()
    assert dados["paginacao"]["limite_por_pagina"] == 300

# Bloco 5 - Validação de data inválida
def test_data_invalida_status(config, params_data_invalida, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_errada" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA ERRADA")
        response = requests.get(url, params=params_data_invalida)
        cache_respostas["cache_data_errada"] = response
    response = cache_respostas["cache_data_errada"] 
    assert response.status_code == 400

def test_erro_data_invalida(config, params_data_invalida, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_errada" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA ERRADA")
        response = requests.get(url, params=params_data_invalida)
        cache_respostas["cache_data_errada"] = response
    response = cache_respostas["cache_data_errada"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_mensagem_data_invalida(config, params_data_invalida, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_errada" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA ERRADA")
        response = requests.get(url, params=params_data_invalida)
        cache_respostas["cache_data_errada"] = response
    response = cache_respostas["cache_data_errada"] 
    dados = response.json()
    print(dados)
    assert "Data invalida" == dados["mensagem"]

# Bloco 6 - Validação de data ausente
def test_data_ausente_status(config, params_data_ausente, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA AUSENTE")
        response = requests.get(url, params=params_data_ausente)
        cache_respostas["cache_data_ausente"] = response
    response = cache_respostas["cache_data_ausente"] 
    assert response.status_code == 400

def test_erro_data_ausente(config, params_data_ausente, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA AUSENTE")
        response = requests.get(url, params=params_data_ausente)
        cache_respostas["cache_data_ausente"] = response
    response = cache_respostas["cache_data_ausente"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_mensagem_data_ausente(config, params_data_ausente, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA AUSENTE")
        response = requests.get(url, params=params_data_ausente)
        cache_respostas["cache_data_ausente"] = response
    response = cache_respostas["cache_data_ausente"] 
    dados = response.json()
    assert "Data invalida" == dados["mensagem"]

# Bloco 7 - Validação de data anterior ao período permitido
def test_data_antiga_status(config, params_data_antiga, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_antiga" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA ANTIGA")
        response = requests.get(url, params=params_data_antiga)
        cache_respostas["cache_data_antiga"] = response
    response = cache_respostas["cache_data_antiga"] 
    assert response.status_code == 400

def test_data_antiga_erro(config, params_data_antiga, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_antiga" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA ANTIGA")
        response = requests.get(url, params=params_data_antiga)
        cache_respostas["cache_data_antiga"] = response
    response = cache_respostas["cache_data_antiga"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_data_antiga_mensagem(config, params_data_antiga, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_antiga" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA ANTIGA")
        response = requests.get(url, params=params_data_antiga)
        cache_respostas["cache_data_antiga"] = response
    response = cache_respostas["cache_data_antiga"] 
    dados = response.json()
    assert dados["mensagem"] == "Você não pode consultar períodos anteriores a 7 dias."

# Bloco 8 - Validação de data superior ao período permitido
def test_data_superior_status(config, params_data_superior, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_superior" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA SUPERIOR")
        response = requests.get(url, params=params_data_superior)
        cache_respostas["cache_data_superior"] = response
    response = cache_respostas["cache_data_superior"] 
    assert response.status_code == 400

def test_data_superior_erro(config, params_data_superior, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_superior" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA SUPERIOR")
        response = requests.get(url, params=params_data_superior)
        cache_respostas["cache_data_superior"] = response
    response = cache_respostas["cache_data_superior"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_data_superior_mensagem(config, params_data_superior, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_data_superior" not in cache_respostas:
        print("FAZENDO REQUEST - GET DATA SUPERIOR")
        response = requests.get(url, params=params_data_superior)
        cache_respostas["cache_data_superior"] = response
    response = cache_respostas["cache_data_superior"] 
    dados = response.json()
    assert dados["mensagem"] == "Data inválida: não é possível consultar datas futuras. Informe uma data entre 08-10-2026 e hoje (15-10-2026), no formato DD-MM-AAAA."

# Bloco 9 - Validação de regime inválido
def test_regime_invalido_status(config, params_regime_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET REGIME INVÁLIDO")
        response = requests.get(url, params=params_regime_invalido)
        cache_respostas["cache_regime_invalido"] = response
    response = cache_respostas["cache_regime_invalido"] 
    assert response.status_code == 400

def test_regime_invalido_erro(config, params_regime_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET REGIME INVÁLIDO")
        response = requests.get(url, params=params_regime_invalido)
        cache_respostas["cache_regime_invalido"] = response
    response = cache_respostas["cache_regime_invalido"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_regime_invalido_mensagem(config, params_regime_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET REGIME INVÁLIDO")
        response = requests.get(url, params=params_regime_invalido)
        cache_respostas["cache_regime_invalido"] = response
    response = cache_respostas["cache_regime_invalido"] 
    dados = response.json()
    assert dados["mensagem"] == "Regime tributário e CRT informados não são compatíveis. Para o regime simples, o CRT deve ser 1 ou 2. Para os regimes real ou presumido, o CRT deve ser 3."

# Bloco 10 - Validação de regime ausente
def test_regime_ausente_status(config, params_regime_ausente, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - GET REGIME AUSENTE")
        response = requests.get(url, params=params_regime_ausente)
        cache_respostas["cache_regime_ausente"] = response
    response = cache_respostas["cache_regime_ausente"] 
    assert response.status_code == 400

def test_regime_ausente_erro(config, params_regime_ausente, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - GET REGIME AUSENTE")
        response = requests.get(url, params=params_regime_ausente)
        cache_respostas["cache_regime_ausente"] = response
    response = cache_respostas["cache_regime_ausente"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_regime_ausente_mensagem(config, params_regime_ausente, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - GET REGIME AUSENTE")
        response = requests.get(url, params=params_regime_ausente)
        cache_respostas["cache_regime_ausente"] = response
    response = cache_respostas["cache_regime_ausente"] 
    dados = response.json()
    assert dados["mensagem"] == "Regime tributário informado não aceito na nossa API. regime pode ser [simples, real, presumido] e crt pode ser [1, 2, 3]"

# Bloco 11 - Validação de CRT inválido
def test_crt_invalido_status(config, params_crt_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET CRT INVÁLIDO")
        response = requests.get(url, params=params_crt_invalido)
        cache_respostas["cache_crt_invalido"] = response
    response = cache_respostas["cache_crt_invalido"] 
    assert response.status_code == 400

def test_crt_invalido_erro(config, params_crt_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET CRT INVÁLIDO")
        response = requests.get(url, params=params_crt_invalido)
        cache_respostas["cache_crt_invalido"] = response
    response = cache_respostas["cache_crt_invalido"]  
    dados = response.json()
    assert dados["erro"] == 1

def test_crt_invalido_erro(config, params_crt_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET CRT INVÁLIDO")
        response = requests.get(url, params=params_crt_invalido)
        cache_respostas["cache_crt_invalido"] = response
    response = cache_respostas["cache_crt_invalido"]  
    dados = response.json()
    assert dados["mensagem"] == f"CRT informado não aceito. Valores aceitos: 1, 2 ou 3 (1 ou 2 para o regime simples; 3 para os regimes real ou presumido). Recebido: \"{params_crt_invalido["crt"]}\"."

# Bloco 12 - Validação de incompatibilidade entre regime e CRT
def test_crt_regime_invalidos_status(config, params_crt_regime_invalidos, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_regime_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - GET CRT E REGIME INVÁLIDOS")
        response = requests.get(url, params=params_crt_regime_invalidos)
        cache_respostas["cache_crt_regime_invalidos"] = response
    response = cache_respostas["cache_crt_regime_invalidos"] 
    assert response.status_code == 400

def test_crt_regime_invalidos_erro(config, params_crt_regime_invalidos, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_regime_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - GET CRT E REGIME INVÁLIDOS")
        response = requests.get(url, params=params_crt_regime_invalidos)
        cache_respostas["cache_crt_regime_invalidos"] = response
    response = cache_respostas["cache_crt_regime_invalidos"]  
    dados = response.json()
    assert dados["erro"] == 1

def test_crt_regime_invalidos_mensagem(config, params_crt_regime_invalidos, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_regime_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - GET CRT INVÁLIDO")
        response = requests.get(url, params=params_crt_regime_invalidos)
        cache_respostas["cache_crt_regime_invalidos"] = response
    response = cache_respostas["cache_crt_regime_invalidos"]  
    dados = response.json()
    assert dados["mensagem"] == "Regime tributário e CRT informados não são compatíveis. Para o regime simples, o CRT deve ser 1 ou 2. Para os regimes real ou presumido, o CRT deve ser 3."

# Bloco 13 - Validação de cMun inválido
def test_cmun_invalido_status(config, params_cmun_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET CMUN INVÁLIDO")
        response = requests.get(url, params=params_cmun_invalido)
        cache_respostas["cache_cmun_invalido"] = response
    response = cache_respostas["cache_cmun_invalido"] 
    assert response.status_code == 400

def test_cmun_invalido_erro(config, params_cmun_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET CMUN INVÁLIDO")
        response = requests.get(url, params=params_cmun_invalido)
        cache_respostas["cache_cmun_invalido"] = response
    response = cache_respostas["cache_cmun_invalido"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_cmun_invalido_mensagem(config, params_cmun_invalido, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET CMUN INVÁLIDO")
        response = requests.get(url, params=params_cmun_invalido)
        cache_respostas["cache_cmun_invalido"] = response
    response = cache_respostas["cache_cmun_invalido"] 
    dados = response.json()
    assert dados["mensagem"] == "cMun inválido. Não encontrado na base de dados ou não pertence ao estado do cliente. Por favor, verifique o cMun."

# Bloco 14 - Validação de página inválida
def test_pagina_invalida_status(config, params_pagina_invalida, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_invalida" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINA INVÁLIDA")
        response = requests.get(url, params=params_pagina_invalida)
        cache_respostas["cache_pagina_invalida"] = response
    response = cache_respostas["cache_pagina_invalida"] 
    assert response.status_code == 400

def test_pagina_invalida_erro(config, params_pagina_invalida, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_invalida" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINA INVÁLIDA")
        response = requests.get(url, params=params_pagina_invalida)
        cache_respostas["cache_pagina_invalida"] = response
    response = cache_respostas["cache_pagina_invalida"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_pagina_invalida_mensagem(config, params_pagina_invalida, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_pagina_invalida" not in cache_respostas:
        print("FAZENDO REQUEST - GET PÁGINA INVÁLIDA")
        response = requests.get(url, params=params_pagina_invalida)
        cache_respostas["cache_pagina_invalida"] = response
    response = cache_respostas["cache_pagina_invalida"] 
    dados = response.json()
    assert dados["mensagem"] == f"pagina inválida. Deve ser um número inteiro a partir de 1. Recebido: \"{params_pagina_invalida["pagina"]}\"."

# Bloco 15 - Validação abaixo do limite mínimo
def test_abaixo_minimo_status(config, params_abaixo_minimo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_abaixo_minimo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE ABAIXO DO MÍNIMO")
        response = requests.get(url, params=params_abaixo_minimo)
        cache_respostas["cache_abaixo_minimo"] = response
    response = cache_respostas["cache_abaixo_minimo"] 
    assert response.status_code == 400

def test_abaixo_minimo_erro(config, params_abaixo_minimo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_abaixo_minimo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE ABAIXO DO MÍNIMO")
        response = requests.get(url, params=params_abaixo_minimo)
        cache_respostas["cache_abaixo_minimo"] = response
    response = cache_respostas["cache_abaixo_minimo"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_abaixo_minimo_mensagem(config, params_abaixo_minimo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_abaixo_minimo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE ABAIXO DO MÍNIMO")
        response = requests.get(url, params=params_abaixo_minimo)
        cache_respostas["cache_abaixo_minimo"] = response
    response = cache_respostas["cache_abaixo_minimo"] 
    dados = response.json()
    assert dados["mensagem"] == f"limite inválido. Deve ser um número inteiro de 1 a 300. Recebido: \"{params_abaixo_minimo["limite"]}\"."

# Bloco 16 - Validação acima do limite máximo
def test_acima_maximo_status(config, params_acima_maximo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_acima_maximo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE ACIMA DO MÁXIMO")
        response = requests.get(url, params=params_acima_maximo)
        cache_respostas["cache_acima_maximo"] = response
    response = cache_respostas["cache_acima_maximo"] 
    assert response.status_code == 400

def test_acima_maximo_erro(config, params_acima_maximo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_acima_maximo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE ACIMA DO MÁXIMO")
        response = requests.get(url, params=params_acima_maximo)
        cache_respostas["cache_acima_maximo"] = response
    response = cache_respostas["cache_acima_maximo"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_acima_maximo_mensagem(config, params_acima_maximo, cache_respostas):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_acima_maximo" not in cache_respostas:
        print("FAZENDO REQUEST - GET LIMITE ACIMA DO MÁXIMO")
        response = requests.get(url, params=params_acima_maximo)
        cache_respostas["cache_acima_maximo"] = response
    response = cache_respostas["cache_acima_maximo"] 
    dados = response.json()
    assert dados["mensagem"] == f"limite inválido. Deve ser um número inteiro de 1 a 300. Recebido: \"{params_acima_maximo["limite"]}\"."

# Bloco 17 - Validação de token inválido
def test_token_invalido_status(url_atualizacoes_token_invalido, params_atualizacoes, cache_respostas):
    if "cache_token_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET TOKEN INVÁLIDO")
        response = requests.get(url_atualizacoes_token_invalido, params=params_atualizacoes)
        cache_respostas["cache_token_invalido"] = response
    response = cache_respostas["cache_token_invalido"] 
    assert response.status_code == 400

def test_token_invalido_erro(url_atualizacoes_token_invalido, params_atualizacoes, cache_respostas):
    if "cache_token_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET TOKEN INVÁLIDO")
        response = requests.get(url_atualizacoes_token_invalido, params=params_atualizacoes)
        cache_respostas["cache_token_invalido"] = response
    response = cache_respostas["cache_token_invalido"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_token_invalido_mensagem(url_atualizacoes_token_invalido, params_atualizacoes, cache_respostas):
    if "cache_token_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET TOKEN INVÁLIDO")
        response = requests.get(url_atualizacoes_token_invalido, params=params_atualizacoes)
        cache_respostas["cache_token_invalido"] = response
    response = cache_respostas["cache_token_invalido"] 
    dados = response.json()
    assert dados["mensagem"] == "Parametros de acesso invalidos"

# Bloco 18 - Validação de CNPJ inválido
def test_cnpj_invalido_status(url_atualizacoes_cnpj_invalido, params_atualizacoes, cache_respostas):
    if "cache_cnpj_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET cnpj INVÁLIDO")
        response = requests.get(url_atualizacoes_cnpj_invalido, params=params_atualizacoes)
        cache_respostas["cache_cnpj_invalido"] = response
    response = cache_respostas["cache_cnpj_invalido"] 
    assert response.status_code == 400

def test_cnpj_invalido_erro(url_atualizacoes_cnpj_invalido, params_atualizacoes, cache_respostas):
    if "cache_cnpj_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET cnpj INVÁLIDO")
        response = requests.get(url_atualizacoes_cnpj_invalido, params=params_atualizacoes)
        cache_respostas["cache_cnpj_invalido"] = response
    response = cache_respostas["cache_cnpj_invalido"] 
    dados = response.json()
    assert dados["erro"] == 1

def test_cnpj_invalido_mensagem(url_atualizacoes_cnpj_invalido, params_atualizacoes, cache_respostas):
    if "cache_cnpj_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - GET cnpj INVÁLIDO")
        response = requests.get(url_atualizacoes_cnpj_invalido, params=params_atualizacoes)
        cache_respostas["cache_cnpj_invalido"] = response
    response = cache_respostas["cache_cnpj_invalido"] 
    dados = response.json()
    assert dados["mensagem"] == "Cliente nao encontrado ou contrato expirado - ff1"