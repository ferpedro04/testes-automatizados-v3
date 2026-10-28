from contratos.contratos_v3 import obter_contrato_documentacao, montar_contrato, normalizar_tipo, identificar_tipo, comparar_tipos, extrair_campos_json, identificar_divergencias_nome
from datetime import datetime
import requests
import pytest 

# Bloco 1 - Montagem do contrato
def test_montagem_contrato():
    arvore = obter_contrato_documentacao()
    contrato_esperado = montar_contrato(arvore, {}, "")
    assert "itens[].produtos.produto.importado" in contrato_esperado
    assert contrato_esperado["itens[].produtos.produto.importado"] == "boolean"

# Bloco 2 - Validação de tipos
def test_normalizacao_tipo():
    assert normalizar_tipo("string, 14") == "string"
    assert normalizar_tipo("boolean") == "boolean"
    assert normalizar_tipo("objeto") == "object"
    assert normalizar_tipo("string, 9 | null") == "string | null"

# Bloco 3 - Validação dos tipos retornados pela API
def test_identificar_tipo():
    assert identificar_tipo(True) == "boolean"
    assert identificar_tipo(123) == "int"
    assert identificar_tipo("7891234567890") == "string"
    assert identificar_tipo([1, 2, 3]) == "array"
    assert identificar_tipo({"ean": "7891234567890"}) == "object"
    assert identificar_tipo(None) == "null"

# Bloco 4 - Validação da comparação dos tipos
def test_comparar_tipos():
    assert comparar_tipos("boolean", "boolean") == "OK"
    assert comparar_tipos("string, 9 | null", "string") == "OK"
    assert comparar_tipos("string, 9 | null", "null") == "OK"
    assert comparar_tipos("boolean", "string") == "TIPO DIVERGENTE"
    assert comparar_tipos("string, 9 | null", "int") == "TIPO DIVERGENTE"

# Bloco 5 - Validação do contrato com respostas reais da API
def test_contrato_retornos_reais(config, retorno_produtos_contrato):
    url = f"{config['url_base']}/revisao/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    cenarios = [
    ("simples", 1),
    ("real", 3),
    ("presumido", 3)
]
    caminhos_unicos = set()
    ufs_validas = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF",
        "ES", "GO", "MA", "MT", "MS", "MG", "PA",
        "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
        "RO", "RR", "SC", "SP", "SE", "TO"
    }
    arvore = obter_contrato_documentacao()
    contrato_esperado = montar_contrato(arvore, {}, "")

    divergencias = []
    campos_nao_documentados = []

    for regime, crt in cenarios:
        produtos_cenario = []
        for produtos in retorno_produtos_contrato:
            produtos_copiados = produtos.copy()
            produtos_copiados["regime"] = regime
            produtos_copiados["crt"] = crt
            if (produtos_copiados["regime"] == "real") or (produtos_copiados["regime"] == "presumido"):
                produtos_copiados["cst"] = "00"
            produtos_cenario.append(produtos_copiados)

        response = requests.post(url, json=produtos_cenario)
        dados = response.json()

        assert response.status_code == 200
        assert dados["erro"] == 0
        assert dados["itens"]
        assert dados["itens_encontrados"] == len(produtos_cenario)

        data_validada = datetime.strptime(dados["dttransacao"], "%d-%m-%Y %H:%M:%S")
        ocorrencias_reais = extrair_campos_json(dados)

        for ocorrencia in ocorrencias_reais:
            ean_produto = None
            caminho_real = ocorrencia["caminho_real"]
            if caminho_real.startswith("itens["):
                indice_produto = int(caminho_real.split("[")[1].split("]")[0])
                ean_produto = dados["itens"][indice_produto]["produtos"]["produto"].get("ean")
            if(ocorrencia["caminho_contrato"] =="itens" and ocorrencia["tipo_real"] == "array"):
                caminho_normalizado = "itens[]"
            elif ocorrencia["caminho_contrato"].startswith("itens[].tributos.imposto_estadual.icms_entrada.por_uf.icms_entrada_"):
                uf = ocorrencia["caminho_contrato"].split("icms_entrada_")[-1]
                if uf in ufs_validas:
                    caminho_normalizado = ("itens[].tributos.imposto_estadual.icms_entrada.por_uf.icms_entrada_UF")
                else:
                    caminho_normalizado = (ocorrencia["caminho_contrato"])
            else:
                caminho_normalizado = (ocorrencia["caminho_contrato"])
            caminhos_unicos.add(caminho_normalizado)
            if caminho_normalizado in contrato_esperado:
                tipo_documentado = contrato_esperado[caminho_normalizado]
                if (caminho_normalizado == "dttransacao") and (tipo_documentado == "datetime"):
                    resultado_comparacao = "OK"
                else:
                    resultado_comparacao = comparar_tipos(tipo_documentado, ocorrencia["tipo_real"])
                if resultado_comparacao != "OK":
                    divergencia = {
                        "caminho_contrato": caminho_normalizado,
                        "caminho_real": ocorrencia["caminho_real"],
                        "tipo_esperado": tipo_documentado,
                        "tipo_real": ocorrencia["tipo_real"],
                        "regime": regime,
                        "status": "TIPO DIVERGENTE",
                        "observacao": "Tipo retornado diferente do documentado",
                        "ean": ean_produto,
                    }
                    divergencias.append(divergencia)
            else:
                campo_nao_documentado = {
                    "caminho_contrato": caminho_normalizado,
                    "caminho_real": ocorrencia["caminho_real"],
                    "tipo_esperado": "Não documentado",
                    "tipo_real": ocorrencia["tipo_real"],
                    "regime": regime,
                    "status": "CAMPO NÃO DOCUMENTADO",
                    "observacao": "Campo retornado pela API sem correspondência na documentação",
                    "ean": ean_produto,
                }
                campos_nao_documentados.append(campo_nao_documentado)
                
    caminhos_somente_api = caminhos_unicos - contrato_esperado.keys()
    caminhos_somente_documentacao = contrato_esperado.keys() - caminhos_unicos
    possiveis_divergencias = identificar_divergencias_nome(caminhos_somente_api, caminhos_somente_documentacao)
    campos_observados = len(contrato_esperado) - len(caminhos_somente_documentacao)
    caminhos_divergentes = {d["caminho_contrato"] for d in divergencias}
    campos_corretos = campos_observados - len(caminhos_divergentes)

    print(f"VALIDAÇÃO DE CONTRATO API V3 | Consolidado | Campos observados: {campos_observados} | Campos não observados: {len(caminhos_somente_documentacao)} | Divergencias: {len(divergencias)} | Divergencias de nome: {len(possiveis_divergencias)} | Campos documentados: {len(contrato_esperado)} | Campos não documentados: {len(caminhos_somente_api)} | Campos corretos: {campos_corretos}")

    if caminhos_somente_documentacao:
        print("\nCAMPOS NÃO OBSERVADOS NA API:")
        for caminho in sorted(caminhos_somente_documentacao):
            tipo_documentado = contrato_esperado[caminho]
            print(f"Campo: {caminho} | Tipo documentado: {tipo_documentado} | Status: CAMPO NÃO ENCONTRADO NA API | Tipo API: Não encontrado | Observação: Campo não observado nos cenários testados; verificar aplicabilidade\n")
    print('\nBUG CONHECIDO | Campo: filiais | Status: CONFIRMADO | '
      'Documentação: array | API: retorna "" quando o campo é omitido | '
      'Contorno temporário: enviar "filiais": [] | Correção: PENDENTE')

    if divergencias:
        print("\nDIVERGÊNCIAS DE TIPO:")
        for divergencia in divergencias:
            print(
                f"\nCampo: {divergencia['caminho_contrato']}"
                f"\nCaminho real: {divergencia['caminho_real']}"
                f"\nDocumentação: {divergencia['tipo_esperado']} | API: {divergencia['tipo_real']}"
                f"\nRegime: {divergencia['regime']} | EAN: {divergencia['ean']}"
                f"\nStatus: {divergencia['status']}"
                f"\nObservação: {divergencia['observacao']}\n"
            )

    if caminhos_somente_api or divergencias or possiveis_divergencias:
        resultado = "CONTRATO COM DIVERGÊNCIAS"
    elif caminhos_somente_documentacao:
        resultado = "COBERTURA PENDENTE"
    else:
        resultado = "SEM DIVERGÊNCIAS NOS CENÁRIOS TESTADOS"
    print(f"\nRESULTADO: {resultado}")

    assert not caminhos_somente_api, {
    "campos_nao_documentados": campos_nao_documentados,
    "possiveis_divergencias_nome": possiveis_divergencias
}
    assert not divergencias, divergencias
    assert caminhos_unicos, "Nenhum campo foi extraído das respostas da API"
    
# Bloco 6 - Validação da extração dos campos do JSON
def test_extrair_campos_json():
    dados = {
    "erro": 0,
    "filiais":	["12345678000199"],
    "itens": [
        {
            "importado": False
        }
    ]
}
    ocorrencias = extrair_campos_json(dados)
    campo_encontrado = False
    filial_encontrada = False
    for ocorrencia in ocorrencias:
        if ocorrencia["caminho_contrato"] == "itens[].importado":
            campo_encontrado = True
            assert ocorrencia["caminho_real"] == "itens[0].importado"
            assert ocorrencia["tipo_real"] == "boolean"
        if ocorrencia["caminho_contrato"] == "filiais[]":
            filial_encontrada = True
            assert ocorrencia["caminho_real"] == "filiais[0]"
            assert ocorrencia["tipo_real"] == "string"
    assert campo_encontrado == True
    assert filial_encontrada == True

# Bloco 7 - Validação de possíveis divergências de nome
def test_identificar_divergencias_nome():
    caminhos_somente_documentacao = {"produto.cod_interno_cliente"}
    caminhos_somente_api = {"produto.codinterno_cliente"}
    resultado = identificar_divergencias_nome(caminhos_somente_api, caminhos_somente_documentacao)
    assert resultado
    assert resultado[0]["status"] == "POSSÍVEL DIVERGÊNCIA DE NOME"

def test_divergencias_nome_estruturas_diferentes():
    caminhos_somente_documentacao = {"produto.cod_interno_cliente"}
    caminhos_somente_api = {"tributos.codinterno_cliente"}  
    resultado = identificar_divergencias_nome(caminhos_somente_api, caminhos_somente_documentacao)
    assert not resultado 

def test_divergencias_nome_sem_similaridade():
    caminhos_somente_documentacao = {"produto.ean"}
    caminhos_somente_api = {"produto.descricao"}  
    resultado = identificar_divergencias_nome(caminhos_somente_api, caminhos_somente_documentacao)
    assert not resultado 