# Imports
import requests
import pytest

# Funções Auxiliares
def gerar_produtos(produto_base, quantidade):
    produtos_teste = []
    codinterno = 0
    for i in range(quantidade):
        codinterno = codinterno + 1
        produto = produto_base[0].copy()
        produto["codinterno"] = codinterno
        produtos_teste.append(produto)
    return produtos_teste

def cnpj_valido(cnpj):
    if len(cnpj) != 14 or not cnpj.isdigit():
        return False
    if len(set(cnpj)) == 1:
        return False
    base = cnpj[:12]
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for digito, peso in zip(base, pesos_1):
        produto_ponderado = int(digito)*peso
        soma = produto_ponderado + soma
    resto = soma % 11
    if resto < 2:
        digito_1 = 0
    else:
        digito_1 = 11 - resto
    base_2 = base + str(digito_1)
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_2 = 0
    for digito, peso in zip(base_2, pesos_2):
        produto_ponderado_2 = int(digito)*peso
        soma_2 = produto_ponderado_2 + soma_2
    resto_2 = soma_2 % 11
    if resto_2 < 2:
        digito_2 = 0
    else:
        digito_2 = 11 - resto_2
    if (digito_1 == int(cnpj[12])) and (digito_2 == int(cnpj[13])):
        return True
    else:
        return False

# Bloco 1 -  Validação de Requisição
def test_status_http(config, retorno_produto_api):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=retorno_produto_api)
    dados = response.json()
    print(dados)
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

# Bloco 7 - Teste de erro para EAN ausente
def test_status_ean_ausente(config, retorno_ean_ausente, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - EAN AUSENTE")
        response = requests.post(url, json=retorno_ean_ausente)
        cache_respostas["cache_ean_ausente"] = response
        response = cache_respostas["cache_ean_ausente"]
        assert response.status_code == 400

def test_erro_ean_ausente(config, retorno_ean_ausente, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - EAN AUSENTE")
        response = requests.post(url, json=retorno_ean_ausente)
        cache_respostas["cache_ean_ausente"] = response
        response = cache_respostas["cache_ean_ausente"]
        dados = response.json()
        assert dados["erro"] == 1

def test_motivo_ean_ausente(config, retorno_ean_ausente, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_ausente" not in cache_respostas:
        print("FAZENDO REQUEST - EAN AUSENTE")
        response = requests.post(url, json=retorno_ean_ausente)
        cache_respostas["cache_ean_ausente"] = response
        response = cache_respostas["cache_ean_ausente"]
        dados = response.json()
        assert "EAN inválido" in dados["mensagem"]

# Bloco 8 - Teste de erro para EAN vazio
def test_status_ean_vazio(config, retorno_ean_vazio, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_vazio" not in cache_respostas:
        print("FAZENDO REQUEST - EAN VAZIO")
        response = requests.post(url, json=retorno_ean_vazio)
        cache_respostas["cache_ean_vazio"] = response
        response = cache_respostas["cache_ean_vazio"]
        assert response.status_code == 400

def test_erro_ean_vazio(config, retorno_ean_vazio, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_vazio" not in cache_respostas:
        print("FAZENDO REQUEST - EAN VAZIO")
        response = requests.post(url, json=retorno_ean_vazio)
        cache_respostas["cache_ean_vazio"] = response
        response = cache_respostas["cache_ean_vazio"]
        dados = response.json()
        assert dados["erro"] == 1

def test_motivo_ean_vazio(config, retorno_ean_vazio, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_vazio" not in cache_respostas:
        print("FAZENDO REQUEST - EAN VAZIO")
        response = requests.post(url, json=retorno_ean_vazio)
        cache_respostas["cache_ean_vazio"] = response
        response = cache_respostas["cache_ean_vazio"]
        dados = response.json()
        assert "EAN inválido" in dados["mensagem"]

# Bloco 9 - Teste de erro para EAN maior que 14
def test_status_ean_maior(config, retorno_ean_maior, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_maior" not in cache_respostas:
        print("FAZENDO REQUEST - EAN MAIOR")
        response = requests.post(url, json=retorno_ean_maior)
        cache_respostas["cache_ean_maior"] = response
        response = cache_respostas["cache_ean_maior"]
        assert response.status_code == 400

def test_erro_ean_maior(config, retorno_ean_maior, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_maior" not in cache_respostas:
        print("FAZENDO REQUEST - EAN MAIOR")
        response = requests.post(url, json=retorno_ean_maior)
        cache_respostas["cache_ean_maior"] = response
        response = cache_respostas["cache_ean_maior"]
        dados = response.json()
        assert dados["erro"] == 1
    
def test_motivo_ean_maior(config, retorno_ean_maior, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_maior" not in cache_respostas:
        print("FAZENDO REQUEST - EAN MAIOR")
        response = requests.post(url, json=retorno_ean_maior)
        cache_respostas["cache_ean_maior"] = response
        response = cache_respostas["cache_ean_maior"]
        dados = response.json()
        assert "EAN inválido" in dados["mensagem"]

# Bloco 10 - Teste de erro para EAN alfanúmerico
def test_status_ean_alfanumerico(config, retorno_ean_alfanumerico, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_alfanumerico" not in cache_respostas:
        print("FAZENDO REQUEST - EAN ALFANÚMERICO")
        response = requests.post(url, json=retorno_ean_alfanumerico)
        cache_respostas["cache_ean_alfanumerico"] = response
        response = cache_respostas["cache_ean_alfanumerico"]
        assert response.status_code == 400

def test_erro_ean_alfanumerico(config, retorno_ean_alfanumerico, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_alfanumerico" not in cache_respostas:
        print("FAZENDO REQUEST - EAN ALFANÚMERICO")
        response = requests.post(url, json=retorno_ean_alfanumerico)
        cache_respostas["cache_ean_alfanumerico"] = response
        response = cache_respostas["cache_ean_alfanumerico"]
        dados = response.json()
        assert dados["erro"] == 1

def test_motivo_ean_alfanumerico(config, retorno_ean_alfanumerico, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_ean_alfanumerico" not in cache_respostas:
        print("FAZENDO REQUEST - EAN ALFANÚMERICO")
        response = requests.post(url, json=retorno_ean_alfanumerico)
        cache_respostas["cache_ean_alfanumerico"] = response
        response = cache_respostas["cache_ean_alfanumerico"]
        dados = response.json()
        assert "EAN inválido" in dados["mensagem"]

# Bloco 11 - Validação de erro para descrição curta
def test_status_descricao_curta(config, retorno_descricao_curta, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_descricao_curta" not in cache_respostas:
        print("FAZENDO REQUEST - DESCRICAO CURTA")
        response = requests.post(url, json=retorno_descricao_curta)
        cache_respostas["cache_descricao_curta"] = response
        response = cache_respostas["cache_descricao_curta"]
        assert response.status_code == 400

def test_erro_descricao_curta(config, retorno_descricao_curta, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_descricao_curta" not in cache_respostas:
        print("FAZENDO REQUEST - DESCRICAO CURTA")
        response = requests.post(url, json=retorno_descricao_curta)
        cache_respostas["cache_descricao_curta"] = response
        response = cache_respostas["cache_descricao_curta"]
        dados = response.json()
        assert dados["erro"] == 1

def test_motivo_descricao_curta(config, retorno_descricao_curta, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_descricao_curta" not in cache_respostas:
        print("FAZENDO REQUEST - DESCRICAO CURTA")
        response = requests.post(url, json=retorno_descricao_curta)
        cache_respostas["cache_descricao_curta"] = response
        response = cache_respostas["cache_descricao_curta"]
        dados = response.json()
        assert "Descrição inválida" in dados["mensagem"]

# Bloco 12 - Validação de descrição válida
def test_status_descricao_valida(config, retorno_descricao_valida, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_descricao_valida" not in cache_respostas:
        print("FAZENDO REQUEST - DESCRICAO VÁLIDA")
        response = requests.post(url, json=retorno_descricao_valida)
        cache_respostas["cache_descricao_valida"] = response
        response = cache_respostas["cache_descricao_valida"]
        assert response.status_code == 200
        
def test_erro_descricao_valida(config, retorno_descricao_valida, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_descricao_valida" not in cache_respostas:
        print("FAZENDO REQUEST - DESCRICAO VÁLIDA")
        response = requests.post(url, json=retorno_descricao_valida)
        cache_respostas["cache_descricao_valida"] = response
        response = cache_respostas["cache_descricao_valida"]
        dados = response.json()
        assert dados["erro"] == 0

# Bloco 13 - Validação de código interno vazio
def test_status_codinterno_vazio(config, retorno_codinterno_vazio, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_vazio" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO VAZIO")
        response = requests.post(url, json=retorno_codinterno_vazio)
        cache_respostas["cache_codinterno_vazio"] = response
        response = cache_respostas["cache_codinterno_vazio"]
        assert response.status_code == 400

def test_erro_codinterno_vazio(config, retorno_codinterno_vazio, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_vazio" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO VAZIO")
        response = requests.post(url, json=retorno_codinterno_vazio)
        cache_respostas["cache_codinterno_vazio"] = response
        response = cache_respostas["cache_codinterno_vazio"]
        dados = response.json()
        assert dados["erro"] == 1

def test_motivo_codinterno_vazio(config, retorno_codinterno_vazio, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_vazio" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO VAZIO")
        response = requests.post(url, json=retorno_codinterno_vazio)
        cache_respostas["cache_codinterno_vazio"] = response
        response = cache_respostas["cache_codinterno_vazio"]
        dados = response.json()
        assert "Código interno do produto não informado" in dados["mensagem"]

# Bloco 14 - Validação de código interno e EAN vazios
def test_status_codinterno_ean_vazios(config, retorno_codinterno_ean_vazios, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_ean_vazios" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN VAZIOS")
        response = requests.post(url, json=retorno_codinterno_ean_vazios)
        cache_respostas["cache_codinterno_ean_vazios"] = response
        response = cache_respostas["cache_codinterno_ean_vazios"]
        assert response.status_code == 400

def test_erro_codinterno_ean_vazios(config, retorno_codinterno_ean_vazios, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_ean_vazios" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN VAZIOS")
        response = requests.post(url, json=retorno_codinterno_ean_vazios)
        cache_respostas["cache_codinterno_ean_vazios"] = response
        response = cache_respostas["cache_codinterno_ean_vazios"]
        dados = response.json()
        assert dados["erro"] == 1

def test_motivo_codinterno_ean_vazios(config, retorno_codinterno_ean_vazios, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_ean_vazios" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN VAZIOS")
        response = requests.post(url, json=retorno_codinterno_ean_vazios)
        cache_respostas["cache_codinterno_ean_vazios"] = response
        response = cache_respostas["cache_codinterno_ean_vazios"]
        dados = response.json()
        assert "Código de barras ou Código interno do produto não enviado ou inválido." in dados["mensagem"]

# Bloco 15 - Validação de código interno e EAN inválidos
def test_status_codinterno_ean_invalidos(config, retorno_codinterno_ean_invalidos, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_ean_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN INVÁLIDOS")
        response = requests.post(url, json=retorno_codinterno_ean_invalidos)
        cache_respostas["cache_codinterno_ean_invalidos"] = response
        response = cache_respostas["cache_codinterno_ean_invalidos"]
        assert response.status_code == 400

def test_erro_codinterno_ean_invalidos(config, retorno_codinterno_ean_invalidos, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_ean_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN INVÁLIDOS")
        response = requests.post(url, json=retorno_codinterno_ean_invalidos)
        cache_respostas["cache_codinterno_ean_invalidos"] = response
    response = cache_respostas["cache_codinterno_ean_invalidos"]
    dados = response.json()
    assert dados["erro"] == 1

def test_motivo_codinterno_ean_invalidos(config, retorno_codinterno_ean_invalidos, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_codinterno_ean_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN INVÁLIDOS")
        response = requests.post(url, json=retorno_codinterno_ean_invalidos)
        cache_respostas["cache_codinterno_ean_invalidos"] = response
        response = cache_respostas["cache_codinterno_ean_invalidos"]
        dados = response.json()
        assert "EAN inválido." in dados["mensagem"]

# Bloco 16 - Retorno de token inválido
def test_status_token_invalido(url_token_invalido, retorno_produto_api, cache_respostas):
    if "cache_codinterno_ean_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN INVÁLIDOS")
        response = requests.post(url_token_invalido, json=retorno_produto_api)
        cache_respostas["cache_codinterno_ean_invalidos"] = response
        response = cache_respostas["cache_codinterno_ean_invalidos"]
        assert response.status_code == 400

def test_erro_token_invalido(url_token_invalido, retorno_produto_api, cache_respostas):
    if "cache_codinterno_ean_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN INVÁLIDOS")
        response = requests.post(url_token_invalido, json=retorno_produto_api)
        cache_respostas["cache_codinterno_ean_invalidos"] = response
        response = cache_respostas["cache_codinterno_ean_invalidos"]
        dados = response.json()
        assert dados["erro"] == 1

def test_retorno_token_invalido(url_token_invalido, retorno_produto_api, cache_respostas):
    if "cache_codinterno_ean_invalidos" not in cache_respostas:
        print("FAZENDO REQUEST - CODINTERNO E EAN INVÁLIDOS")
        response = requests.post(url_token_invalido, json=retorno_produto_api)
        cache_respostas["cache_codinterno_ean_invalidos"] = response
        response = cache_respostas["cache_codinterno_ean_invalidos"]
        dados = response.json()
        assert "Parametros de acesso invalidos" in dados["mensagem"]
   

# Bloco 17 - Retorno de token ausente
def test_status_token_ausente(url_token_ausente, retorno_produto_api):
    response = requests.post(url_token_ausente, json=retorno_produto_api)
    assert response.status_code == 404

# Bloco 18 - Retorno de CNPJ inválido
def test_status_cnpj_invalido(url_cnpj_invalido, retorno_produto_api, cache_respostas):
    if "cache_cnpj_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CNPJ INVÁLIDO")
        response = requests.post(url_cnpj_invalido, json=retorno_produto_api)
        cache_respostas["cache_cnpj_invalido"] = response
        response = cache_respostas["cache_cnpj_invalido"]
        assert response.status_code == 400

def test_erro_cnpj_invalido(url_cnpj_invalido, retorno_produto_api, cache_respostas):
    if "cache_cnpj_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CNPJ INVÁLIDO")
        response = requests.post(url_cnpj_invalido, json=retorno_produto_api)
        cache_respostas["cache_cnpj_invalido"] = response
        dados = response.json()
        assert dados["erro"] == 1

def test_retorno_cnpj_invalido(url_cnpj_invalido, retorno_produto_api, cache_respostas):
    if "cache_cnpj_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CNPJ INVÁLIDO")
        response = requests.post(url_cnpj_invalido, json=retorno_produto_api)
        cache_respostas["cache_cnpj_invalido"] = response
        dados = response.json()
        assert "Cliente nao encontrado ou contrato expirado - ff1" in dados["mensagem"]

# Bloco 19 - Retorno de ID inválido
def test_status_id_invalido(url_id_invalido, retorno_produto_api, cache_respostas):
   if "cache_id_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - ID INVÁLIDO")
        response = requests.post(url_id_invalido, json=retorno_produto_api)
        cache_respostas["cache_id_invalido"] = response
        response = cache_respostas["cache_id_invalido"]
        assert response.status_code == 400

def test_erro_id_invalido(url_id_invalido, retorno_produto_api, cache_respostas):
    if "cache_id_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - ID INVÁLIDO")
        response = requests.post(url_id_invalido, json=retorno_produto_api)
        cache_respostas["cache_id_invalido"] = response
        dados = response.json()
        assert dados["erro"] == 1
    
def test_retorno_id_invalido(url_id_invalido, retorno_produto_api, cache_respostas):
    if "cache_id_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - ID INVÁLIDO")
        response = requests.post(url_id_invalido, json=retorno_produto_api)
        cache_respostas["cache_id_invalido"] = response
        dados = response.json()
        assert "ID do Parceiro invalido" in dados["mensagem"]


# Bloco 20 - Retorno de regime inválido
def test_status_regime_invalido(config, retorno_regime_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - REGIME INVÁLIDO")
        response = requests.post(url, json=retorno_regime_invalido)
        cache_respostas["cache_regime_invalido"] = response
        response = cache_respostas["cache_regime_invalido"]
        assert response.status_code == 400

def test_erro_regime_invalido(config, retorno_regime_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - REGIME INVÁLIDO")
        response = requests.post(url, json=retorno_regime_invalido)
        cache_respostas["cache_regime_invalido"] = response
        response = cache_respostas["cache_regime_invalido"]
        assert response.status_code == 400
        dados = response.json()
        assert dados["erro"] == 1

def test_retorno_regime_invalido(config, retorno_regime_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_regime_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - REGIME INVÁLIDO")
        response = requests.post(url, json=retorno_regime_invalido)
        cache_respostas["cache_regime_invalido"] = response
        response = cache_respostas["cache_regime_invalido"]
        assert response.status_code == 400
        dados = response.json()
        assert "Regime tributário informado não aceito" in dados["mensagem"]
    

# Bloco 21 - Retorno de CRT inválido
def test_status_crt_invalido(config, retorno_crt_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CRT INVÁLIDO")
        response = requests.post(url, json=retorno_crt_invalido)
        cache_respostas["cache_crt_invalido"] = response
        response = cache_respostas["cache_crt_invalido"]
        assert response.status_code == 400

def test_erro_crt_invalido(config, retorno_crt_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CRT INVÁLIDO")
        response = requests.post(url, json=retorno_crt_invalido)
        cache_respostas["cache_crt_invalido"] = response
        response = cache_respostas["cache_crt_invalido"]
        assert response.status_code == 400
        dados = response.json()
        assert dados["erro"] == 1

def test_retorno_crt_invalido(config, retorno_crt_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CRT INVÁLIDO")
        response = requests.post(url, json=retorno_crt_invalido)
        cache_respostas["cache_crt_invalido"] = response
        response = cache_respostas["cache_crt_invalido"]
        assert response.status_code == 400
        dados = response.json()
        assert "Regime tributário e CRT informados não são compatíveis." in dados["mensagem"]
    

# Bloco 22 - Retorno de CRT e regime incompátiveis
def test_status_crt_regime_incompativeis(config, retorno_crt_regime_incompativeis, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_regime_incompativeis" not in cache_respostas:
        print("FAZENDO REQUEST - CRT E REGIME INCOMPÁTIVEIS")
        response = requests.post(url, json=retorno_crt_regime_incompativeis)
        cache_respostas["cache_crt_regime_incompativeis"] = response
        response = cache_respostas["cache_crt_regime_incompativeis"]
        assert response.status_code == 400

def test_erro_crt_regime_incompativeis(config, retorno_crt_regime_incompativeis, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_regime_incompativeis" not in cache_respostas:
        print("FAZENDO REQUEST - CRT E REGIME INCOMPÁTIVEIS")
        response = requests.post(url, json=retorno_crt_regime_incompativeis)
        cache_respostas["cache_crt_regime_incompativeis"] = response
        response = cache_respostas["cache_crt_regime_incompativeis"]
        dados = response.json()
        assert dados["erro"] == 1

def test_retorno_crt_regime_incompativeis(config, retorno_crt_regime_incompativeis, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_crt_regime_incompativeis" not in cache_respostas:
        print("FAZENDO REQUEST - CRT E REGIME INCOMPÁTIVEIS")
        response = requests.post(url, json=retorno_crt_regime_incompativeis)
        cache_respostas["cache_crt_regime_incompativeis"] = response
        response = cache_respostas["cache_crt_regime_incompativeis"]
        dados = response.json()
        assert "Regime tributário e CRT informados não são compatíveis." in dados["mensagem"]
   

# Bloco 23 - Retorno cMun inválido
def test_status_cmun_invalido(config, retorno_cmun_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CMUN INVÁLIDO")
        response = requests.post(url, json=retorno_cmun_invalido)
        cache_respostas["cache_cmun_invalido"] = response
        response = cache_respostas["cache_cmun_invalido"]
        assert response.status_code == 400

def test_erro_cmun_invalido(config, retorno_cmun_invalido, cache_respostas):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CMUN INVÁLIDO")
        response = requests.post(url, json=retorno_cmun_invalido)
        cache_respostas["cache_cmun_invalido"] = response
        response = cache_respostas["cache_cmun_invalido"]
        dados = response.json()
        assert dados["erro"] == 1

def test_retorno_cmun_invalido(config, retorno_cmun_invalido, cache_respostas):
   url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
   if "cache_cmun_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CMUN INVÁLIDO")
        response = requests.post(url, json=retorno_cmun_invalido)
        cache_respostas["cache_cmun_invalido"] = response
        response = cache_respostas["cache_cmun_invalido"]
        dados = response.json()
        assert "cMun inválido." in dados["mensagem"]


# Bloco 24 - Retorno cMun digitos errados
@pytest.mark.parametrize("cmun_invalido", [
    "123456",
    "12345678"
])
def test_status_cmun_tamanho_invalido(config, cmun_invalido, retorno_produto_api, cache_respostas):
    produto = retorno_produto_api[0].copy()
    produto["cMun"] = cmun_invalido
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_tamanho_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CMUN TAMANHO INVÁLIDO")
        response = requests.post(url, json=cmun_invalido)
        cache_respostas["cache_cmun_tamanho_invalido"] = response
        response = cache_respostas["cache_cmun_tamanho_invalido"]
        assert response.status_code == 400
        
@pytest.mark.parametrize("cmun_invalido", [
    "123456",
    "12345678"
])
def test_erro_cmun_tamanho_invalido(config, cmun_invalido, retorno_produto_api, cache_respostas):
    produto = retorno_produto_api[0].copy()
    produto["cMun"] = cmun_invalido
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_tamanho_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CMUN TAMANHO INVÁLIDO")
        response = requests.post(url, json=cmun_invalido)
        cache_respostas["cache_cmun_tamanho_invalido"] = response
        response = cache_respostas["cache_cmun_tamanho_invalido"]
        dados = response.json()
        assert dados["erro"] == 1

@pytest.mark.parametrize("cmun_invalido", [
    "123456",
    "12345678"
])
def test_retorno_cmun_tamanho_invalido(config, cmun_invalido, retorno_produto_api, cache_respostas):
    produto = retorno_produto_api[0].copy()
    produto["cMun"] = cmun_invalido
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    if "cache_cmun_tamanho_invalido" not in cache_respostas:
        print("FAZENDO REQUEST - CMUN TAMANHO INVÁLIDO")
        response = requests.post(url, json=cmun_invalido)
        cache_respostas["cache_cmun_tamanho_invalido"] = response
        response = cache_respostas["cache_cmun_tamanho_invalido"]
        dados = response.json()
        assert "cMun inválido. Deve conter 7 dígitos numéricos." in dados["mensagem"]

# Bloco 25 - Retorno de requisição sem produto
def test_status_produto_vazio(config):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[])
    assert response.status_code == 400

def test_erro_produto_vazio(config):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[])
    dados = response.json()
    assert dados["erro"] == 1

def test_retorno_produto_vazio(config):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[])
    dados = response.json()
    assert "Nenhum item encontrado" in dados["mensagem"]


# Bloco 26 - Teste de 1 produto(já validado na  etapa 1)

# Bloco 27 - Teste de 299 produtos
def test_status_299_produtos(config, retorno_produto_api):
    produtos_teste_299 = gerar_produtos(retorno_produto_api, 299)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_299)
    assert response.status_code == 200

def test_erro_299_produtos(config, retorno_produto_api):
    produtos_teste_299 = gerar_produtos(retorno_produto_api, 299)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_299)
    dados = response.json()
    assert dados["erro"] == 0

def test_enviados_299_produtos(config, retorno_produto_api):
    produtos_teste_299 = gerar_produtos(retorno_produto_api, 299)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_299)
    dados = response.json()
    produtos_enviados = dados["itens_enviados"]
    assert produtos_enviados == len(produtos_teste_299)

def test_encontrados_299_produtos(config, retorno_produto_api):
    produtos_teste_299 = gerar_produtos(retorno_produto_api, 299)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_299)
    dados = response.json()
    produtos_encontrados = dados["itens_encontrados"]
    assert produtos_encontrados == len(produtos_teste_299)

# Bloco 28 - Teste de 300 produtos
def test_status_300_produtos(config, retorno_produto_api):
    produtos_teste_300 = gerar_produtos(retorno_produto_api, 300)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_300)
    assert response.status_code == 200
    

def test_erro_300_produtos(config, retorno_produto_api):
    produtos_teste_300 = gerar_produtos(retorno_produto_api, 300)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_300)
    dados = response.json()
    assert dados["erro"] == 0

def test_enviados_300_produtos(config, retorno_produto_api):
    produtos_teste_300 = gerar_produtos(retorno_produto_api, 300)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_300)
    dados = response.json()
    produtos_enviados = dados["itens_enviados"]
    assert produtos_enviados == len(produtos_teste_300)

def test_encontrados_300_produtos(config, retorno_produto_api):
    produtos_teste_300 = gerar_produtos(retorno_produto_api, 300)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_300)
    dados = response.json()
    produtos_encontrados = dados["itens_encontrados"]
    assert produtos_encontrados == len(produtos_teste_300)

# Bloco 29 - Teste para mais de 300 produtos
def test_status_350_produtos(config, retorno_produto_api):
    produtos_teste_350 = gerar_produtos(retorno_produto_api, 350)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_350)
    assert response.status_code == 400

def test_erro_350_produtos(config, retorno_produto_api):
    produtos_teste_350 = gerar_produtos(retorno_produto_api, 350)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_350)
    dados = response.json()
    assert dados["erro"] == 1

def test_retorno_350_produtos(config, retorno_produto_api):
    produtos_teste_350 = gerar_produtos(retorno_produto_api, 350)
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=produtos_teste_350)
    dados = response.json()
    assert "Limite de itens excedido! Limite por envio: 300" in dados["mensagem"]

# Bloco 30 - Validação de filiais válidas
def test_status_filiais(config, retorno_produto_api):
    produto = retorno_produto_api[0].copy()
    produto["filiais"] = [
    "11292330000114",
    "61728826000166",
    "07859313000149"
    ]
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[produto])
    assert response.status_code == 200

def test_erro_filiais(config, retorno_produto_api):
    produto = retorno_produto_api[0].copy()
    produto["filiais"] = [
    "11292330000114",
    "61728826000166",
    "07859313000149"
    ]
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[produto])
    dados = response.json()
    assert dados["erro"] == 0

def test_retorno_filiais(config, retorno_produto_api):
    produto = retorno_produto_api[0].copy()
    produto["filiais"] = [
    "11292330000114",
    "61728826000166",
    "07859313000149"
    ]
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[produto])
    dados = response.json()
    assert dados["filiais"] == produto["filiais"]

# Bloco 30 - Validação de filiais inválidas
@pytest.mark.xfail(
    reason="Bug conhecido: API aceita filial inválida e retorna 200. Esperado: 404.",
    strict=True,
)
def test_status_filiais_invalidas(config, retorno_produto_api):
    produto = retorno_produto_api[0].copy()
    produto["filiais"] = [
    "12345678912345"]
    cnpj_filial_invalido = produto["filiais"][0]
    assert cnpj_valido(cnpj_filial_invalido) is False
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[produto])
    assert response.status_code == 404

@pytest.mark.xfail(
    reason="Bug conhecido: API aceita filial inválida e retorna 200. Esperado: 404.",
    strict=True,
)
def test_erro_filiais_invalidas(config, retorno_produto_api):
    produto = retorno_produto_api[0].copy()
    produto["filiais"] = [
    "12345678912345"]
    cnpj_filial_invalido = produto["filiais"][0]
    assert cnpj_valido(cnpj_filial_invalido) is False
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[produto])
    dados = response.json()
    assert dados["erro"] == 1
    
@pytest.mark.xfail(
    reason="Bug conhecido: API aceita filial inválida e retorna 200. Esperado: 404.",
    strict=True,
)
def test_retorno_filiais_invalidas(config, retorno_produto_api):
    produto = retorno_produto_api[0].copy()
    produto["filiais"] = [
    "12345678912345"]
    cnpj_filial_invalido = produto["filiais"][0]
    assert cnpj_valido(cnpj_filial_invalido) is False
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.post(url, json=[produto])
    dados = response.json()
    assert "Filial inválida" in dados["mensagem"]
   