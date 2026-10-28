# Imports
from dotenv import load_dotenv
from difflib import SequenceMatcher
import requests
import os
import json
import pytest

# Carregamento da ENV
load_dotenv()
docs_usuario = os.getenv("DOCS_USUARIO")
docs_senha = os.getenv("DOCS_SENHA")

# Bloco 1 - Autenticação e acesso à documentação da API V3
def obter_contrato_documentacao():
    url_sessao = "https://figurafiscalws.com.br/v3.0/api/session.php"
    url_login = "https://figurafiscalws.com.br/v3.0/api/login.php"
    url_documentacao = "https://figurafiscalws.com.br/v3.0/docs-page.html"

    sessao = requests.Session()

    response = sessao.get(url_sessao, timeout=10)
    assert response.status_code == 200

    dados = response.json()
    csrf = dados.get("csrf", "")

    payload_login = {
        "usuario": docs_usuario,
        "senha": docs_senha,
        "partner": "avantfiscal",
        "csrf": csrf,
        "require_doc_access": True
    }

    response_login = sessao.post(url_login, json=payload_login, timeout=10)
    assert response_login.status_code == 200

    dados_login = response_login.json()
    assert dados_login["ok"] is True

    response_docs = sessao.get(url_documentacao, timeout=10)
    assert response_docs.status_code == 200

    html_documentacao = response_docs.text
    assert "FF_JSON_TREE" in html_documentacao

    inicio_arvore = html_documentacao.find("window.FF_JSON_TREE =")
    assert inicio_arvore != -1

    inicio_json = html_documentacao.find("[", inicio_arvore)
    assert inicio_json != -1

    trecho_json = html_documentacao[inicio_json:]
    decoder = json.JSONDecoder()
    arvore, fim_json = decoder.raw_decode(trecho_json)

    return arvore

# Bloco 2 - Conversão da árvore em contrato
def montar_contrato(arvore, contrato, caminho_pai):
    for campo in arvore:
        nome = campo[0]
        tipo = campo[1]

        if caminho_pai:
            caminho_completo = f"{caminho_pai}.{nome}"
        else:
            caminho_completo = nome

        contrato.update({caminho_completo: tipo})

        if len(campo) == 4:
            filhos = campo[3]
            montar_contrato(filhos, contrato, caminho_completo)
    return contrato

# Bloco 3 - Normalização dos tipos documentados
def normalizar_tipo(tipo_documento):
    partes = tipo_documento.split(",")
    tipo_base = partes[0].strip()
    if "null" in tipo_documento:
        tipo_base = tipo_base + " | null"
    if tipo_base == "objeto":
        tipo_base = "object"
    return tipo_base

# Bloco 4 - Identificar tipos
def identificar_tipo(valor):
    if type(valor) == bool:
        return "boolean"
    if type(valor) == int:
        return "int"
    if type(valor) == str:
        return "string"
    if type(valor) == list:
        return "array"
    if type(valor) == dict:
        return "object"
    if valor is None:
        return "null"


# Bloco 5 - Comparação dos tipos documentados e retornados pela API
def comparar_tipos(tipo_documento, tipo_real):
    tipo_esperado = normalizar_tipo(tipo_documento)
    tipos_permitidos = tipo_esperado.split("|")
    for tipo in tipos_permitidos:
        if tipo.strip() == tipo_real:
            return "OK"
    return "TIPO DIVERGENTE"

# Bloco 6 - Extração dos caminhos e tipos do JSON real
def extrair_campos_json(dados):
    ocorrencias = []
    def percorrer_json(valor_atual, caminho_contrato, caminho_real):
        if type(valor_atual) == dict:
            for chave, valor in valor_atual.items():
                if caminho_contrato:
                    novo_caminho_contrato = f"{caminho_contrato}.{chave}"
                else:
                    novo_caminho_contrato = chave
                if caminho_real:
                    novo_caminho_real = f"{caminho_real}.{chave}"
                else:
                    novo_caminho_real = chave
                tipo_real = identificar_tipo(valor)
                adesao_ocorrencias = {"caminho_contrato":novo_caminho_contrato, "caminho_real":novo_caminho_real, "tipo_real":tipo_real}
                ocorrencias.append(adesao_ocorrencias)
                percorrer_json(valor, novo_caminho_contrato, novo_caminho_real)
        if type(valor_atual) == list:
            for indice, elemento in enumerate(valor_atual):
                    caminho_real_elemento = f"{caminho_real}[{indice}]"
                    caminho_contrato_elemento = f"{caminho_contrato}[]"
                    tipo_elemento = identificar_tipo(elemento)
                    if (tipo_elemento != "object") and (tipo_elemento != "array"):
                        adesao_ocorrencias = {"caminho_contrato":caminho_contrato_elemento, "caminho_real":caminho_real_elemento, "tipo_real":tipo_elemento}
                        ocorrencias.append(adesao_ocorrencias)
                    percorrer_json(elemento, caminho_contrato_elemento, caminho_real_elemento)
    percorrer_json(dados, "", "")
    return ocorrencias 

# Bloco 7 - Identificação de possíveis divergências de nome
def identificar_divergencias_nome(caminho_somente_api, caminho_somente_documentacao):
    possiveis_divergencias = []
    for caminho_documentado in caminho_somente_documentacao:
        partes_documentadas = caminho_documentado.rsplit(".", 1)
        if len(partes_documentadas) == 2:
            caminho_pai_documentado = partes_documentadas[0]
            nome_campo_documentado = partes_documentadas[1]
        else:
            caminho_pai_documentado = ""
            nome_campo_documentado = partes_documentadas[0]
        for caminho_api in caminho_somente_api:
            partes_api = caminho_api.rsplit(".", 1)
            if len(partes_api) == 2:
                caminho_pai_api = partes_api[0]
                nome_campo_api = partes_api[1]
            else:
                caminho_pai_api = ""
                nome_campo_api = partes_api[0]
            if caminho_pai_documentado == caminho_pai_api:
                similaridade = SequenceMatcher(None, nome_campo_documentado, nome_campo_api).ratio()
                if similaridade >= 0.80:
                    possivel_divergencia= {"campo_documentado":caminho_documentado,
                                           "campo_api":caminho_api,
                                           "similaridade":similaridade,
                                           "status":"POSSÍVEL DIVERGÊNCIA DE NOME"}
                    possiveis_divergencias.append(possivel_divergencia)
    return possiveis_divergencias