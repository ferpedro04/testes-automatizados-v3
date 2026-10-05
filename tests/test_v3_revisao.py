# Imports
import requests

# Bloco 1 -  Validação de Requisição
def test_status_http(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    assert response.status_code == 200
    
def test_erro(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    assert dados["erro"] == 0

def test_produtos_enviados(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    produtos_enviados = dados["itens_enviados"]
    assert produtos_enviados == 1

# Bloco 2 - Validação do retorno
def test_produtos_encontrados(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    produtos_encontrados = dados["itens_encontrados"]
    assert produtos_encontrados == 1

def test_produtos_existentes(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    assert "itens" in dados

def test_quantidade_produtos(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    quantidade_produtos = len(dados["itens"])
    assert quantidade_produtos == 1

# Bloco 3 - Validação do conteúdo
def test_regime_tributario(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    regime_tributario = dados["regime_tributario"].lower()
    assert regime_tributario == config["regime"]

def test_crt(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    crt = dados["crt"]
    assert crt == config["crt"]

def test_cmun(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    cmun = dados["cMun"]
    assert cmun == config["cmun"]

def test_informacoes_produto(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    produtos = dados["itens"][0]["produtos"]
    assert "produto" in produtos
    produto = produtos["produto"]
    assert "ean" in produto
    assert "descricao" in produto
    assert "idProduto" in produto

def test_informacoes_tributarias(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    tributos = dados["itens"][0]["tributos"]
    assert tributos

# Bloco 4 - Validação de múltiplos produtos
def test_status_multiplos_produtos(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    assert response.status_code == 200

def test_erro_multiplos_produtos(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    assert dados["erro"] == 0

def test_enviados_multiplos_produtos(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    produtos_enviados = dados["itens_enviados"]
    assert produtos_enviados == len(retorno_produtos_multiplos_testes)

# Bloco 5 - Validação do retorno de múltiplos produtos
def test_encontrados_multiplos_produtos(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    produtos_encontrados = dados["itens_encontrados"]
    assert produtos_encontrados == len(retorno_produtos_multiplos_testes)

def test_existentes_multiplos_produtos(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    assert "itens" in dados

def test_quantidade_multiplos_produtos(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    quantidade_produtos = len(dados["itens"])
    assert quantidade_produtos == len(retorno_produtos_multiplos_testes)

# Bloco 6 - Validação do conteúdo de Múltiplos produtos
def test_informacoes_multplos_testes(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    for item in dados["itens"]:
        produtos = item["produtos"]
        assert "produto" in produtos
        produto = produtos["produto"]
        assert "ean" in produto
        assert "descricao" in produto
        assert "idProduto" in produto

def test_informacoes_tributarias_multiplos_testes(config, retorno_produtos_multiplos_testes):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produtos_multiplos_testes)
    dados = response.json()
    for item in dados["itens"]:
        tributos = item["tributos"]
        assert tributos