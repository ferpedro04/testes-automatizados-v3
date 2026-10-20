# Imports
import requests
import pytest
from datetime import datetime


# Configuração - Isolamento dos testes de Rate Limit
pytestmark = pytest.mark.rate_limit

# Funções auxiliares - Validação das respostas de bloqueio
def validar_resposta_bloqueio(response):
    dados = response.json()
    inicio_bloqueio = datetime.fromisoformat(dados["bloqueio_iniciado_em"])
    fim_bloqueio = datetime.fromisoformat(dados["liberado_em"])
    duracao_bloqueio = fim_bloqueio - inicio_bloqueio
    conversao_minutos = duracao_bloqueio.total_seconds() / 60
    assert dados["erro"] == 1
    assert dados["mensagem"] == "CNPJ temporariamente bloqueado devido ao excesso de requisições inválidas."
    assert isinstance(dados["minutos_bloqueio"], int)
    assert dados["minutos_bloqueio"] > 0
    assert isinstance(dados["aguardar_segundos"], int)
    assert dados["aguardar_segundos"] >= 0
    assert fim_bloqueio > inicio_bloqueio
    assert conversao_minutos == dados["minutos_bloqueio"]

# Bloco 1 - Validação de requisições inválidas consecutivas em Atualizações
def test_rate_limit_atualizacoes(config_rl, params_abaixo_minimo):
    url = f"{config_rl['url_base']}/atualizacoes/{config_rl['id_parceiro']}/{config_rl['cnpj']}/{config_rl['token']}"
    respostas = []

    response = requests.get(url, params=params_abaixo_minimo)
    respostas.append(response)

    response = requests.get(url, params=params_abaixo_minimo)
    respostas.append(response)

    response = requests.get(url, params=params_abaixo_minimo)
    respostas.append(response)

    bloqueio_encontrado = False
    for tentativa, response in enumerate(respostas, start=1):
        print(f"Tentativa {tentativa}: HTTP {response.status_code}")
        print(f"Resposta {tentativa}: {response.json()}")
        retry_after = response.headers.get("Retry-After")
        print(f"Tentativa {tentativa} - Retry-After: {retry_after}")
        assert response.status_code in (400, 429)
        if response.status_code == 429:
            bloqueio_encontrado = True
            validar_resposta_bloqueio(response)
            dados = response.json()
            assert "limite inválido" in dados["motivo"]
            assert dados["rota"] == "atualizacao"
            assert retry_after
            valores = retry_after.split(",")
            assert int(valores[0]) == dados["aguardar_segundos"]
    assert bloqueio_encontrado
            
# Bloco 2 - Validação de requisições inválidas consecutivas em Revisão
def test_rate_limit_revisao(config_rl, retorno_ean_alfanumerico):
    url = f"{config_rl['url_base']}/revisao/{config_rl['id_parceiro']}/{config_rl['cnpj']}/{config_rl['token']}"
    respostas = []

    response = requests.post(url, json=retorno_ean_alfanumerico)
    respostas.append(response)

    response = requests.post(url, json=retorno_ean_alfanumerico)
    respostas.append(response)

    response = requests.post(url, json=retorno_ean_alfanumerico)
    respostas.append(response)

    bloqueio_encontrado = False
    for tentativa, response in enumerate(respostas, start=1):
        print(f"Tentativa {tentativa}: HTTP {response.status_code}")
        print(f"Resposta {tentativa}: {response.json()}")
        retry_after = response.headers.get("Retry-After")
        print(f"Tentativa {tentativa} - Retry-After: {retry_after}")
        assert response.status_code in (400, 429)
        if response.status_code == 429:
            bloqueio_encontrado = True
            validar_resposta_bloqueio(response)
            dados = response.json()
            assert "EAN inválido" in dados["motivo"]
            assert dados["rota"] == "revisao"
            assert retry_after
            valores = retry_after.split(",")
            assert int(valores[0]) == dados["aguardar_segundos"]
    assert bloqueio_encontrado

# Bloco 3 - Validação do reset de erros consecutivos em Atualizações
def test_reset_rate_limit_atualizacoes(config_rl, params_minimo, params_abaixo_minimo):
    url = f"{config_rl['url_base']}/atualizacoes/{config_rl['id_parceiro']}/{config_rl['cnpj']}/{config_rl['token']}"
    response_preparacao = requests.get(url, params=params_minimo)
    assert response_preparacao.status_code == 200
    response_invalida = requests.get(url, params=params_abaixo_minimo)
    assert response_invalida.status_code == 400
    response_invalida_2 = requests.get(url, params=params_abaixo_minimo)
    assert response_invalida_2.status_code == 400
    response_valida = requests.get(url, params=params_minimo)
    assert response_valida.status_code == 200
    response_invalida_3 = requests.get(url, params=params_abaixo_minimo)
    assert response_invalida_3.status_code == 429

# Bloco 4 - Validação do reset de erros consecutivos em Revisão
def test_reset_rate_limit_revisao(config_rl, retorno_produto_api, retorno_ean_alfanumerico):
    url = f"{config_rl['url_base']}/revisao/{config_rl['id_parceiro']}/{config_rl['cnpj']}/{config_rl['token']}"
    response_preparacao_revisao = requests.post(url, json=retorno_produto_api)
    assert response_preparacao_revisao.status_code == 200
    response_invalida_revisao = requests.post(url, json=retorno_ean_alfanumerico)
    assert response_invalida_revisao.status_code == 400
    response_invalida_2_revisao = requests.post(url, json=retorno_ean_alfanumerico)
    assert response_invalida_2_revisao.status_code == 400
    response_valida_revisao = requests.post(url, json=retorno_produto_api)
    assert response_valida_revisao.status_code == 200
    response_invalida_3_revisao = requests.post(url, json=retorno_ean_alfanumerico)
    assert response_invalida_3_revisao.status_code == 429
    