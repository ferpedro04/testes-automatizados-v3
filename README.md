# Suíte de Testes Automatizados — API V3.0 | Avant Fiscal

## Objetivo

Esta suíte de testes automatizados tem como objetivo validar o comportamento e os retornos das requisições realizadas aos endpoints da API V3.0 da Avant Fiscal:

- **POST `/revisao`** — Revisão Fiscal de produtos.
- **GET `/atualizacoes`** — Consulta de atualizações fiscais.

Os testes verificam o processamento das requisições, os status HTTP, os códigos de erro, as mensagens retornadas, a estrutura do JSON e as informações fiscais dos produtos.

A suíte contempla cenários positivos e negativos, incluindo validação de credenciais, parâmetros obrigatórios, dados tributários, limites de requisição, paginação e mecanismos de bloqueio por requisições inválidas.

Também contempla a **validação automatizada de contrato da API V3**, responsável por comparar a estrutura real do JSON retornado com os campos, caminhos e tipos definidos na documentação.

O objetivo é identificar comportamentos inesperados, divergências entre documentação e implementação, prevenir regressões após atualizações da API e contribuir para a confiabilidade dos serviços disponibilizados pela Avant Fiscal.

O projeto foi estruturado para permitir que outros integrantes da equipe executem a regressão, investiguem falhas e acrescentem novos cenários conforme a evolução da API V3.

---

## Tecnologias utilizadas

- **Python** — Linguagem utilizada no desenvolvimento da suíte de testes.
- **Pytest** — Framework utilizado para criação e execução dos testes automatizados.
- **Requests** — Biblioteca utilizada para realizar requisições HTTP à API.
- **Python-dotenv** — Biblioteca utilizada para carregar as variáveis de ambiente armazenadas no arquivo `.env`.
- **Difflib (SequenceMatcher)** — Biblioteca nativa do Python utilizada para identificar possíveis divergências de nomenclatura entre campos da API e da documentação.

---

## Estrutura do projeto

```text
projeto/
├── tests/
│   ├── contratos/
│   │   └── contratos_v3.py
│   ├── conftest.py
│   ├── test_v3_revisao.py
│   ├── test_v3_atualizacao.py
│   ├── test_v3_rate_limit.py
│   └── test_v3_contrato.py
├── .env
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

- **`tests/conftest.py`** — Centraliza configurações, dados de teste e fixtures compartilhadas entre as suítes.
- **`tests/test_v3_revisao.py`** — Contém os testes positivos e negativos do endpoint de Revisão Fiscal.
- **`tests/test_v3_atualizacao.py`** — Contém os testes positivos e negativos do endpoint de Atualizações, incluindo paginação e validação de parâmetros.
- **`tests/test_v3_rate_limit.py`** — Contém os testes específicos do mecanismo de bloqueio dos endpoints de Revisão e Atualizações, além da liberação administrativa do CNPJ.
- **`tests/test_v3_contrato.py`** — Contém os testes automatizados da validação de contrato, incluindo comparação com os retornos reais da API e testes das funções auxiliares.
- **`tests/contratos/contratos_v3.py`** — Contém as funções responsáveis pela construção do contrato esperado, extração dos campos do JSON, comparação dos tipos e identificação de possíveis divergências de nome.
- **`.env`** — Armazena configurações e credenciais de acesso à API, incluindo as credenciais exclusivas de Rate Limit e a autorização administrativa. Não deve ser versionado.
- **`.env.example`** — Modelo das variáveis de ambiente necessárias para executar o projeto, sem credenciais reais.
- **`.gitignore`** — Define os arquivos e diretórios que não devem ser versionados.
- **`pytest.ini`** — Registra o marcador `rate_limit` e configura a exclusão desses testes da execução padrão.
- **`requirements.txt`** — Lista as dependências e versões utilizadas no projeto.
- **`README.md`** — Documenta a instalação, configuração, execução, resultados e manutenção da suíte.

---

## Instalação e configuração

### 1. Criar e ativar o ambiente virtual

O ambiente virtual (`venv`) cria um espaço isolado para as dependências do projeto, evitando conflitos com outros projetos ou com a instalação global do Python.

Para criar o ambiente virtual, execute:

```powershell
python -m venv venv
```

Para ativá-lo no PowerShell do Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

Com o ambiente virtual ativo, execute:

```powershell
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as bibliotecas utilizadas pelo projeto e suas respectivas versões.

### 3. Configurar as variáveis de ambiente

O projeto utiliza o arquivo `.env` para armazenar configurações e credenciais de acesso à API.

Após clonar o repositório, crie um arquivo `.env` na raiz do projeto, utilizando `.env.example` como referência.

Exemplo:

```env
URL_BASE=
ID_PARCEIRO=
CNPJ=
TOKEN=
CMUN=
REGIME=
CRT=
CNPJ_RATE_LIMIT=
TOKEN_RATE_LIMIT=
TOKEN_LIBERACAO_RATE_LIMIT=
OPERADOR_RATE_LIMIT=
```

As variáveis `CNPJ` e `TOKEN` são utilizadas na regressão padrão.

As variáveis `CNPJ_RATE_LIMIT` e `TOKEN_RATE_LIMIT` identificam as credenciais exclusivas dos testes de bloqueio.

A variável `TOKEN_LIBERACAO_RATE_LIMIT` armazena a chave de autorização necessária para acessar a rota interna de liberação de penalidades.

A variável `OPERADOR_RATE_LIMIT` identifica o responsável pela execução da liberação. Cada integrante da equipe deve preencher esse campo com seu próprio nome.

O IP público é obtido automaticamente durante a preparação da requisição administrativa.

**Importante:** o arquivo `.env` contém credenciais sensíveis e não deve ser enviado ao GitHub ou compartilhado publicamente.

Durante a revisão de 28/10/2026, foi confirmado que o arquivo `.env` está incluído no `.gitignore` e não está sendo rastreado pelo Git. Essa verificação não substitui uma auditoria do histórico de commits ou de credenciais eventualmente inseridas em outros arquivos.

---

## Organização dos testes

O projeto separa os testes de Revisão Fiscal, Atualizações, Rate Limit e Validação de Contrato em arquivos diferentes.

As configurações e fixtures compartilhadas são centralizadas em `conftest.py`, facilitando a reutilização dos dados e a manutenção da suíte.

### Isolamento dos testes de Rate Limit

Os testes de Rate Limit são mantidos em `tests/test_v3_rate_limit.py` e identificados pelo marcador `pytest.mark.rate_limit`.

O arquivo `pytest.ini` utiliza a configuração:

```ini
[pytest]
markers =
    rate_limit: testes que provocam bloqueio temporario na API

addopts = -m "not rate_limit"
```

Essa configuração exclui os testes de Rate Limit da regressão padrão.

O objetivo é impedir que a execução habitual da suíte provoque bloqueios temporários no CNPJ utilizado nos testes de Revisão Fiscal e Atualizações.

As requisições de Rate Limit utilizam credenciais específicas, carregadas pelas variáveis `CNPJ_RATE_LIMIT` e `TOKEN_RATE_LIMIT`.

Diferentemente das validações de regressão que reutilizam respostas em cache, os testes de Rate Limit realizam requisições HTTP reais e consecutivas, pois precisam observar o comportamento do mecanismo de bloqueio.

A liberação administrativa também fica isolada e deve ser executada explicitamente.

### Reutilização de requisições

A regressão utiliza uma fixture de cache para armazenar respostas HTTP e reutilizá-las entre testes que compartilham o mesmo cenário.

Esse mecanismo evita requisições repetidas desnecessariamente, especialmente quando diferentes testes validam o status HTTP, o código de erro e a mensagem de uma mesma resposta.

Cada cenário utiliza uma chave própria no cache, evitando misturar respostas de requisições diferentes.

O cache funciona durante a execução configurada da suíte e não representa armazenamento permanente entre execuções independentes.

Nos testes de Rate Limit, as respostas das requisições consecutivas são armazenadas em listas locais, permitindo validar cada tentativa sem impedir novas chamadas HTTP.

### Organização da validação de contrato

A validação de contrato utiliza duas responsabilidades principais:

- **Funções auxiliares:** construir o contrato esperado e realizar a comparação entre a documentação e as ocorrências extraídas do JSON.
- **Testes automatizados:** verificar o funcionamento dessas funções e comparar o contrato com respostas reais da API V3.

O contrato esperado utiliza os caminhos completos dos campos, considerando a hierarquia de objetos e arrays.

A validação real contempla os regimes Simples Nacional, Lucro Real e Lucro Presumido, consolidando os resultados em um único relatório.

O teste utiliza cópias dos produtos para preparar cada requisição sem modificar os dados originais da fixture.

Os registros de divergência preservam informações como regime tributário, caminho real e EAN do produto, quando disponível.

---

## Executando os testes

Os testes são executados utilizando o **Pytest**, que identifica automaticamente arquivos e funções seguindo o padrão de nomenclatura `test_`.

### Executar toda a regressão padrão

```powershell
python -m pytest tests/ -v
```

Esse comando executa os testes de Revisão Fiscal, Atualizações e Validação de Contrato, excluindo os testes de Rate Limit por meio da configuração do `pytest.ini`.

### Executar somente Revisão Fiscal

```powershell
python -m pytest tests/test_v3_revisao.py -v -s
```

### Executar somente Atualizações

```powershell
python -m pytest tests/test_v3_atualizacao.py -v -s -rs
```

### Executar somente Validação de Contrato

```powershell
python -m pytest tests/test_v3_contrato.py -v -s
```

Esse comando executa os testes de contrato e as validações das funções auxiliares.

### Executar somente o contrato com retornos reais

```powershell
python -m pytest tests/test_v3_contrato.py::test_contrato_retornos_reais -v -s
```

Esse comando executa a comparação do contrato documentado com as respostas reais da API V3, considerando os três regimes tributários definidos no teste.

O relatório consolidado é apresentado no terminal.

### Executar um teste específico

Exemplo com um teste de Revisão Fiscal:

```powershell
python -m pytest tests/test_v3_revisao.py::test_quantidade_multiplos_produtos -v -s
```

Exemplo com um teste de Atualizações:

```powershell
python -m pytest tests/test_v3_atualizacao.py::test_data_invalida_status -v -s
```

### Executar vários testes específicos

```powershell
python -m pytest tests/test_v3_atualizacao.py::test_token_invalido_status tests/test_v3_atualizacao.py::test_token_invalido_erro tests/test_v3_atualizacao.py::test_token_invalido_mensagem -v -s
```

### Verificar os testes disponíveis

Para listar os testes selecionados sem executar requisições:

```powershell
python -m pytest --collect-only -q
```

Para consultar somente os testes de Rate Limit:

```powershell
python -m pytest tests/test_v3_rate_limit.py -m rate_limit --collect-only -q
```

### Opções utilizadas nos comandos

- **`-v`** — Exibe detalhadamente cada teste e seu resultado.
- **`-s`** — Permite visualizar as mensagens exibidas com `print()` durante a execução.
- **`-rs`** — Exibe os motivos dos testes marcados como `SKIPPED`.
- **`-m rate_limit`** — Seleciona os testes identificados pelo marcador `rate_limit`, sobrescrevendo a exclusão padrão configurada no projeto.
- **`--collect-only`** — Identifica e lista os testes sem executá-los.

---

## Como adicionar novos testes e cenários

Para adicionar novos cenários à suíte automatizada, siga o padrão de organização existente.

### 1. Identificar o endpoint ou funcionalidade

Antes de desenvolver o novo teste, identifique qual funcionalidade será validada.

- Testes relacionados à Revisão Fiscal devem ficar em `test_v3_revisao.py`.
- Testes relacionados às Atualizações devem ficar em `test_v3_atualizacao.py`.
- Testes que provocam bloqueios devem ficar em `test_v3_rate_limit.py`.
- Testes de comparação do contrato devem ficar em `test_v3_contrato.py`.
- Funções auxiliares de contrato devem ser mantidas em `tests/contratos/contratos_v3.py`.

### 2. Definir o cenário esperado

Identifique qual comportamento precisa ser validado.

O cenário pode ser positivo, quando a API deve processar corretamente a requisição, ou negativo, quando deve rejeitar informações inválidas e retornar o erro esperado.

Antes de escrever o `assert`, confirme o comportamento esperado conforme a regra de negócio ou o contrato da API.

### 3. Reutilizar fixtures existentes

Sempre que possível, utilize as fixtures disponíveis no `conftest.py`.

Caso o cenário exija novos dados, adicione uma fixture apropriada, evitando repetir informações em diferentes arquivos.

As credenciais de acesso devem continuar sendo carregadas pelas variáveis de ambiente.

### 4. Implementar o teste

As funções devem utilizar o prefixo `test_`, permitindo sua identificação automática pelo Pytest.

Exemplo básico:

```python
# Bloco - Validação de novo cenário em Atualizações
def test_novo_cenario(config, params_minimo):
    url = f"{config['url_base']}/atualizacoes/{config['id_parceiro']}/{config['cnpj']}/{config['token']}"
    response = requests.get(url, params=params_minimo)

    assert response.status_code == 200
```

Esse exemplo demonstra apenas a estrutura de uma validação HTTP.

Novos cenários devem incluir `asserts` adicionais conforme o resultado esperado, como códigos de erro, mensagens e campos específicos do JSON.

Quando diferentes testes validarem a mesma requisição, avalie a reutilização da resposta pelo mecanismo de cache existente.

### 5. Executar o teste individualmente

Antes de executar toda a regressão, valide somente a função implementada.

Exemplo:

```powershell
python -m pytest tests/test_v3_atualizacao.py::test_novo_cenario -v -s
```

Verifique se os `asserts` correspondem ao comportamento esperado.

### 6. Executar a regressão completa

Após validar o novo cenário, execute:

```powershell
python -m pytest tests/ -v
```

O objetivo é garantir que a alteração não comprometeu os testes existentes.

### 7. Atualizar a documentação

Caso o novo teste represente uma funcionalidade, limite, regra de negócio ou comportamento relevante ainda não documentado, atualize o README.

**Importante:** novos cenários de Rate Limit devem respeitar o isolamento configurado no projeto. Não utilize `pytest.skip()` para ocultar falhas reais da API.

---

## Entendendo os resultados

Cada teste utiliza `assert` para comparar o comportamento da API com o resultado esperado.

Exemplo:

```python
assert response.status_code == 200
```

O Pytest apresenta os seguintes resultados:

- **PASSED** — O teste foi executado e todas as validações passaram.
- **FAILED** — Uma validação falhou ou ocorreu um erro inesperado durante o teste.
- **SKIPPED** — O cenário não foi executado por uma condição previamente identificada.
- **XFAILED** — O teste apresentou uma falha esperada, previamente identificada e documentada.
- **XPASSED** — Um teste marcado como falha esperada passou, indicando a necessidade de revisar essa marcação.
- **DESELECTED** — O teste foi identificado, mas excluído da execução por um filtro ou configuração.

Ao final da execução, o Pytest apresenta um resumo dos resultados.

**Importante:** testes `SKIPPED`, `XFAILED` e `DESELECTED` não devem ser contabilizados como testes aprovados.

---

## Como investigar falhas nos testes

Quando um teste apresentar `FAILED`, o Pytest informa o arquivo, a função, a linha da falha e os valores obtidos e esperados na comparação.

Exemplo:

```text
assert response.status_code == 200
E assert 400 == 200
```

Nesse cenário, o teste esperava HTTP 200, mas recebeu HTTP 400.

### Procedimento de investigação

1. Identifique qual teste falhou e qual `assert` provocou a falha.
2. Compare o resultado esperado com a resposta real da API.
3. Verifique os parâmetros, as credenciais e os dados enviados.
4. Consulte o corpo JSON da resposta para identificar mensagens e motivos.
5. Confirme se houve alteração intencional na regra de negócio ou no contrato da API.
6. Verifique se existe alguma dependência de massa de dados ou do estado do ambiente.
7. Caso o comportamento seja inesperado, registre as evidências e comunique ao responsável pelo endpoint.

Falhas relacionadas à ausência de massa de dados devem ser diferenciadas de erros reais de processamento.

Nos testes de Rate Limit, também é necessário verificar se o CNPJ possui penalidades ou contadores acumulados.

Caso o estado inicial esteja comprometido, utilize o Bloco 5 de Rate Limit para realizar a liberação autorizada antes de iniciar uma nova bateria.

**Importante:** um teste com resultado `FAILED` não significa automaticamente que existe um defeito na API. Também pode indicar dados de teste incorretos, ambiente inadequado ou uma expectativa desatualizada.

Não altere um `assert` apenas para transformar uma execução `FAILED` em `PASSED` sem confirmar o comportamento esperado.

---

## Cenários validados

### 1. Revisão Fiscal — API V3

O arquivo `test_v3_revisao.py` contempla validações relacionadas ao processamento de produtos enviados para revisão fiscal.

Entre os cenários implementados estão:

- Requisições com credenciais válidas e inválidas.
- Revisão com um único produto.
- Revisão com múltiplos produtos.
- Validação dos status HTTP.
- Validação de códigos de erro e mensagens.
- Quantidade de produtos enviados e encontrados.
- Existência e estrutura dos itens retornados.
- Informações principais dos produtos.
- Informações tributárias dos produtos.
- Validação de `regime_tributario`, `crt` e `cMun`.
- Cenários com produtos vazios ou informações inválidas.
- Validação de lotes com 299, 300 e 350 produtos.
- Validações de informações relacionadas a filiais.
- Registro de falhas esperadas conhecidas por meio do Pytest.

### 2. Atualizações — API V3

O arquivo `test_v3_atualizacao.py` contempla consultas de atualizações fiscais, validação de parâmetros e mecanismos de paginação.

**Cenários positivos:**

- Consulta com data válida.
- Consulta com parâmetros válidos.
- Retorno da primeira página.
- Utilização dos parâmetros `pagina` e `limite`.
- Limite mínimo de 1 registro.
- Limite máximo de 300 registros.
- Validação dos metadados de paginação.
- Validação da quantidade de itens retornados.
- Navegação entre páginas quando existem atualizações suficientes.

**Cenários negativos:**

- Data inválida.
- Data ausente.
- Data anterior ao período permitido.
- Data futura.
- Regime tributário inválido.
- Regime tributário ausente.
- CRT inválido.
- Combinação incompatível entre regime e CRT.
- `cMun` inválido.
- Página inválida.
- Limite inferior ao permitido.
- Limite superior a 300.
- Token inválido.
- CNPJ inválido.

**Estrutura de paginação validada:**

- `pagina_atual`
- `limite_por_pagina`
- `total_registros`
- `total_paginas`
- `proxima_pagina`

### 3. Tratamento da ausência de atualizações

O endpoint de Atualizações consulta informações que podem variar diariamente conforme os dados disponíveis na base.

Por esse motivo, determinados testes de paginação dependem da existência de registros suficientes para realizar a validação.

Quando a API retorna uma condição específica de ausência de atualizações necessárias ao cenário, os testes correspondentes utilizam `pytest.skip()`.

Durante a regressão de 28/10/2026, foi identificado que a segunda página poderia retornar HTTP 400 com uma mensagem informando a existência de apenas uma página.

O tratamento foi ajustado para reconhecer as condições conhecidas de massa insuficiente, incluindo mensagens de ausência de atualizações e de existência de apenas uma página, sem ignorar indiscriminadamente outros erros HTTP.

Essa estratégia evita falhas indevidas exclusivamente pela indisponibilidade de massa de dados.

O `skip` não deve ser utilizado para ocultar erros HTTP inesperados, problemas de autenticação ou falhas reais da API.

Os cenários que exigem massa de dados controlada poderão ser executados novamente quando houver um ambiente de homologação adequado.

### 4. Validação automatizada de contrato — API V3

O arquivo `test_v3_contrato.py` implementa a validação do contrato de retorno da API V3, comparando os campos documentados com as respostas reais do endpoint `/revisao`.

O objetivo é responder:

**O JSON retornado pela API V3 está de acordo com a estrutura e os tipos definidos na documentação?**

#### Construção do contrato esperado

As funções auxiliares disponíveis em `tests/contratos/contratos_v3.py` são utilizadas para obter a representação da documentação e montar o contrato esperado.

Cada campo é identificado pelo caminho completo no JSON, juntamente com o tipo documentado.

Exemplos:

```text
erro
regime_tributario
itens[].produtos.produto.ean
itens[].produtos.produto.importado
itens[].tributos.imposto_estadual.icms_saida.cst
itens[].tributos.imposto_federal.pis.pis_saida.cst
```

A notação `itens[]` representa os elementos de um array, permitindo comparar a mesma estrutura independentemente da posição de cada produto.

#### Extração e normalização dos campos

A função `extrair_campos_json()` percorre a resposta real da API e identifica as ocorrências dos campos, incluindo seus caminhos e tipos.

A normalização considera situações específicas do contrato, como:

- Representação do array `itens[]`.
- Preservação da hierarquia de objetos e arrays.
- Normalização dos caminhos de ICMS por UF, considerando as unidades federativas válidas.

A comparação utiliza o caminho normalizado para localizar o campo correspondente no contrato documentado.

#### Comparação dos tipos

A função `comparar_tipos()` verifica a compatibilidade entre o tipo esperado e o tipo identificado no retorno.

São consideradas as representações documentadas de:

- String.
- Inteiro.
- Booleano.
- Array.
- Objeto.
- Valores nulos, quando previstos pelo contrato.

O campo `dttransacao` recebe tratamento específico, com validação do formato de data e hora documentado:

```text
DD-MM-AAAA HH:mm:ss
```

A validação utiliza `datetime.strptime()` para verificar a conversão da string retornada.

Campos que apresentam tipos incompatíveis são registrados com o status:

```text
TIPO DIVERGENTE
```

#### Campos não encontrados na API

Quando um campo documentado não aparece no conjunto de respostas analisadas, ele é registrado como:

```text
CAMPO NÃO ENCONTRADO NA API
```

Essa classificação indica ausência nos cenários executados, não necessariamente um defeito da API.

Campos condicionais podem depender de produtos ou situações tributárias específicas.

#### Campos não documentados

Quando a API retorna um campo cujo caminho não existe no contrato esperado, ele é registrado como:

```text
CAMPO NÃO DOCUMENTADO
```

O registro contém o caminho, tipo retornado, regime, produto quando identificável, status e observação.

Esse comportamento foi validado utilizando um campo fictício adicionado temporariamente ao JSON em memória durante um teste controlado.

O campo simulado foi removido após a validação.

#### Possíveis divergências de nome

A função `identificar_divergencias_nome()` utiliza `SequenceMatcher` para procurar nomes semelhantes entre campos exclusivos da API e campos documentados não encontrados.

A comparação considera somente campos pertencentes ao mesmo caminho pai.

Foi adotado um limite inicial de similaridade de 80% para sinalização.

Os campos identificados recebem o status:

```text
POSSÍVEL DIVERGÊNCIA DE NOME
```

A identificação não significa que os campos são automaticamente equivalentes.

A funcionalidade foi validada com testes que verificam:

- Nomes semelhantes na mesma estrutura.
- Nomes semelhantes em estruturas diferentes.
- Nomes com similaridade insuficiente.

#### Cenários executados

O teste de contrato utiliza sete produtos e executa a consulta nos três regimes tributários:

| Regime | CRT | Produtos |
|---|---:|---:|
| Simples Nacional | 1 | 7 |
| Lucro Real | 3 | 7 |
| Lucro Presumido | 3 | 7 |

Total: **21 consultas de produto distribuídas em três requisições**, considerando os sete produtos enviados em cada regime.

Cada regime utiliza uma cópia independente dos produtos.

Para os cenários de Lucro Real e Lucro Presumido, o campo `cst` é informado conforme a validação exigida pela API.

O objetivo é ampliar a diversidade das respostas analisadas.

A quantidade de produtos e regimes não representa, por si só, comprovação de cobertura de todas as regras fiscais possíveis.

#### Consolidação dos resultados

Os caminhos identificados nos três regimes são reunidos em um conjunto (`set`), evitando contabilizar campos repetidos.

As divergências mantêm seus registros individuais, permitindo identificar ocorrências por regime e produto.

O relatório diferencia:

- Campos documentados.
- Campos observados.
- Campos sem divergências de tipo detectadas.
- Campos não observados.
- Campos não documentados.
- Ocorrências de divergência de tipo.
- Possíveis divergências de nome.

As ocorrências repetidas de um mesmo caminho não são confundidas com campos distintos.

#### Identificação do produto

Quando uma divergência ocorre dentro do array `itens`, o teste utiliza o índice presente no caminho real para localizar o produto correspondente.

O EAN é incluído nos registros quando disponível.

Assim, o relatório consegue apresentar:

- Caminho documentado.
- Caminho real.
- Tipo esperado.
- Tipo retornado.
- Regime tributário.
- EAN do produto.
- Status.
- Observação.

Campos gerais da resposta não necessariamente possuem EAN associado.

#### Relatório consolidado

A validação apresenta um resumo único no terminal, após processar os três regimes.

Também apresenta os campos não observados e as divergências de tipo identificadas.

O resultado geral pode assumir:

```text
CONTRATO COM DIVERGÊNCIAS
COBERTURA PENDENTE
SEM DIVERGÊNCIAS NOS CENÁRIOS TESTADOS
```

As condições são diferenciadas conforme a presença de inconsistências e a cobertura dos campos documentados.

**O resultado `PASSED` não significa que todos os campos condicionais foram exercitados.** Significa que as validações obrigatórias implementadas foram aprovadas nos cenários executados.

#### Resultado da validação

Na execução consolidada registrada em 28/10/2026, foram identificados:

| Indicador | Quantidade |
|---|---:|
| Campos documentados | 151 |
| Caminhos observados | 147 |
| Campos não observados | 4 |
| Campos não documentados | 0 |
| Possíveis divergências de nome | 0 |

Os quatro campos não observados pertencem ao grupo:

```text
itens[].tributos.imposto_estadual.icms_entrada.cargaliquida_cnae
```

Os caminhos não observados são:

```text
itens[].tributos.imposto_estadual.icms_entrada.cargaliquida_cnae
itens[].tributos.imposto_estadual.icms_entrada.cargaliquida_cnae.pFCPST
itens[].tributos.imposto_estadual.icms_entrada.cargaliquida_cnae.pST
itens[].tributos.imposto_estadual.icms_entrada.cargaliquida_cnae.por_uf
```

Esses campos permanecem como cobertura não observada nos cenários utilizados, devendo ter sua aplicabilidade verificada com uma massa adequada quando necessário.

Durante o desenvolvimento, uma divergência de tipo no campo `icms_saida.dispositivoLegal` foi identificada e corrigida pelo desenvolvedor responsável.

Após a correção, o teste de contrato voltou a apresentar `PASSED`.

#### Bug conhecido — filiais

Foi identificado que o campo `filiais`, documentado como `array`, apresentava comportamento divergente quando omitido da requisição.

O retorno observado era uma string vazia (`""`), enquanto o envio explícito de `filiais: []` produzia um array vazio.

O comportamento foi confirmado com o desenvolvedor responsável.

Como contorno temporário autorizado, a fixture de contrato envia:

```python
produto_copiado["filiais"] = []
```

O contorno permite a continuidade da validação de contrato, mas não representa a correção definitiva do comportamento da API.

**Situação:** bug conhecido, correção pendente.

---

## Resultados das execuções

### Regressão padrão — 28/10/2026

Na execução conjunta registrada em 28/10/2026, foram apresentados:

| Resultado | Quantidade |
|---|---:|
| PASSED | 150 |
| SKIPPED | 4 |
| XFAILED | 3 |
| DESELECTED | 5 |
| FAILED inesperados | 0 |

**Tempo de execução:** 140,30 segundos (aproximadamente 2 minutos e 20 segundos).

A execução apresentou 157 resultados de testes selecionados, considerando os aprovados, pulados e falhas esperadas, além de cinco testes não selecionados.

Os testes `DESELECTED` não foram executados nessa rodada e não devem ser contabilizados como aprovados.

Os testes especiais de Rate Limit permaneceram excluídos da regressão padrão, conforme a configuração de isolamento.

As quatro ocorrências de `SKIPPED` estão associadas a cenários dependentes de massa de dados suficiente para paginação.

As três ocorrências de `XFAILED` correspondem a falhas esperadas já identificadas na suíte de Revisão Fiscal.

### Evolução da regressão

Na execução anterior, registrada em 20/10/2026:

| Resultado | Quantidade |
|---|---:|
| Testes de regressão selecionados | 148 |
| PASSED | 141 |
| SKIPPED | 4 |
| XFAILED | 3 |
| FAILED inesperados | 0 |

A implementação posterior incluiu a validação automatizada de contrato e ajustes nos testes existentes.

Os resultados podem variar conforme alterações na API, documentação e massa de dados.

### Resultados do Rate Limit

Na execução conjunta realizada em 20/10/2026, os quatro testes de Rate Limit foram aprovados.

| Resultado | Quantidade |
|---|---:|
| Testes executados | 4 |
| PASSED | 4 |
| FAILED | 0 |

**Tempo registrado na execução conjunta:** 19,99 segundos.

O Bloco 5 também foi executado individualmente e apresentou `PASSED`, com retorno HTTP 200.

Os resultados correspondem às execuções registradas e podem variar conforme alterações posteriores no código, na API e no estado dos contadores.

---

## Problemas e comportamentos identificados durante o desenvolvimento

Durante a implementação da suíte automatizada, foram identificadas situações que exigiram investigação, ajustes nos testes ou esclarecimento das regras de negócio.

Nem todas essas situações representam defeitos da API. Algumas correspondem a limitações do ambiente de testes ou comportamentos previstos na implementação.

### 1. Mensagens de datas dinâmicas

O endpoint `/atualizacoes` retorna mensagens de erro contendo datas calculadas em relação ao dia atual.

Inicialmente, uma validação utilizava datas fixas, o que fazia o teste falhar em execuções posteriores.

**Solução aplicada:** utilização de `datetime` e `timedelta` para calcular dinamicamente as datas esperadas.

Também foi necessário preservar a formatação exata das mensagens retornadas pela API, incluindo os parênteses utilizados na apresentação da data atual.

### 2. Dependência da massa de dados na paginação

Alguns testes de paginação dependem da existência de registros suficientes na base de dados para validar a navegação entre páginas.

Na ausência desses registros, determinados cenários não podem ser concluídos.

Durante a regressão de 28/10/2026, foi identificada uma resposta HTTP 400 informando que a consulta possuía apenas uma página, com limite de cinco registros.

A validação anterior reconhecia somente uma mensagem específica de ausência de atualizações.

**Tratamento aplicado:** ajuste da condição de `pytest.skip()` para contemplar as mensagens conhecidas de massa insuficiente, sem ignorar genericamente qualquer erro de paginação.

O comportamento foi identificado como uma limitação da massa disponível no cenário, não como defeito automaticamente confirmado na API.

### 3. Falhas esperadas em Revisão Fiscal

Durante o desenvolvimento da suíte, foram identificados cenários de Revisão Fiscal que apresentam comportamentos conhecidos e ainda não tratados como resultados aprovados.

Esses cenários foram identificados por meio de `pytest.xfail()`, permitindo diferenciar falhas conhecidas de regressões inesperadas.

Na regressão de 28/10/2026, três testes apresentaram `XFAILED`.

As causas específicas devem ser consultadas nos testes e nas respectivas marcações, evitando registrar causas não confirmadas.

### 4. Persistência do histórico de bloqueios

Foi identificado que o encerramento do tempo de bloqueio não reinicia automaticamente o histórico de penalidades do CNPJ.

Esse comportamento provocava respostas HTTP 429 em cenários que esperavam inicialmente HTTP 400.

**Solução aplicada:** criação do Bloco 5 de Rate Limit, utilizando a rota administrativa autorizada para liberar os registros de penalidade e contagem antes de novas baterias.

Esse comportamento foi esclarecido com o desenvolvedor responsável e não deve ser classificado como defeito da API.

### 5. Header Retry-After com valores repetidos

Durante os testes de Rate Limit, foram observadas respostas com valores duplicados no header `Retry-After`, como `600, 600`.

A implementação atual valida o primeiro valor do header e sua correspondência com o campo `aguardar_segundos`.

A duplicação foi comunicada ao desenvolvedor responsável e não foi tratada como bloqueadora da entrega.

Esse comportamento permanece registrado como uma observação técnica, sem afirmar que houve correção na API.

### 6. Preservação do motivo original do bloqueio

Durante os testes, foi observado que o campo `motivo` continua exibindo o erro responsável pelo início do bloqueio, mesmo quando novas requisições inválidas são enviadas durante a penalidade.

Por exemplo, um bloqueio provocado por `limite=-10` pode continuar apresentando esse motivo mesmo após uma tentativa posterior com outro valor inválido.

O comportamento foi esclarecido com o desenvolvedor responsável e considerado esperado.

**Tratamento aplicado:** os testes validam o tipo de erro relacionado ao bloqueio, sem exigir que o campo `motivo` reproduza os parâmetros da requisição mais recente.

### 7. Divergência de contrato — dispositivoLegal

Durante o desenvolvimento da validação de contrato, foi identificada uma divergência no campo:

```text
itens[].tributos.imposto_estadual.icms_saida.dispositivoLegal
```

A documentação indicava o tipo `string`, enquanto a API retornava `null` para o produto de EAN `9788598078373`.

A ocorrência foi reproduzida nos três regimes tributários.

O teste registrou:

- Caminho documentado e caminho real.
- Tipo esperado e tipo retornado.
- EAN do produto.
- Regimes afetados.
- Status `TIPO DIVERGENTE`.

A divergência foi encaminhada ao desenvolvedor responsável, Joca.

**Resultado:** após a correção realizada em 28/10/2026, o teste foi executado novamente e apresentou `PASSED`.

Esse caso demonstrou a capacidade da suíte de identificar inconsistências reais de contrato e validar a correção posteriormente.

### 8. Bug conhecido — filiais

O campo `filiais` apresentou retorno incompatível com o tipo documentado quando omitido da requisição.

**Comportamento identificado:**

- Documentação: `array`.
- Campo omitido: retorno como string vazia.
- Campo enviado como `[]`: retorno como array vazio.

O problema foi confirmado com o desenvolvedor responsável.

**Tratamento temporário:** envio de `filiais: []` na massa de testes.

**Situação:** correção definitiva pendente na API.

### 9. Campos condicionais não observados

A validação consolidada identificou quatro campos do grupo `cargaliquida_cnae` que não apareceram nas respostas dos sete produtos, analisados nos três regimes.

Esses campos foram classificados como:

```text
CAMPO NÃO ENCONTRADO NA API
```

A classificação representa ausência nos cenários executados, não confirmação de defeito.

**Situação:** cobertura pendente de massa de dados que permita observar a estrutura, quando aplicável.

---

## Cuidados para manutenção

Ao adicionar novos testes ao projeto:

- Manter cenários de Revisão, Atualizações, Rate Limit e Contrato em seus respectivos arquivos.
- Centralizar configurações e credenciais nas fixtures apropriadas e no `.env`.
- Evitar incluir credenciais reais diretamente no código.
- Reutilizar respostas armazenadas no cache quando os cenários utilizarem a mesma requisição.
- Preservar testes independentes e executáveis individualmente sempre que possível.
- Verificar o comportamento esperado na API antes de definir os `asserts`.
- Não utilizar `pytest.skip()` para esconder defeitos reais.
- Documentar falhas conhecidas com `pytest.xfail()` somente quando houver justificativa.
- Executar a regressão completa após alterações significativas na suíte.
- Evitar executar testes que provocam bloqueios utilizando credenciais da regressão padrão.
- Não incluir a chave de autorização administrativa no código-fonte ou no repositório.
- Manter o README atualizado conforme novos cenários sejam implementados.

Para os testes de contrato:

- Atualizar a representação do contrato quando a documentação da API for modificada.
- Preservar a comparação dos caminhos completos e dos tipos.
- Não considerar automaticamente nomes semelhantes como equivalentes.
- Não tratar campos condicionais ausentes como bugs sem investigação.
- Registrar novas divergências com evidências de produto, regime e retorno.
- Não criar exceções para forçar a aprovação de campos divergentes sem confirmação da regra esperada.
- Manter documentados os contornos temporários e removê-los quando a API for corrigida.

---

## Testes de Rate Limit — API V3

O Rate Limit é um mecanismo de proteção da API que controla requisições inválidas e aplica bloqueios temporários quando determinadas condições são atingidas.

A suíte automatizada contempla os endpoints:

- **POST `/revisao`**
- **GET `/atualizacoes`**

Os testes de bloqueio utilizam um CNPJ específico, separado daquele empregado na regressão padrão.

### Comportamento do mecanismo

Conforme as regras confirmadas com o desenvolvedor responsável, o mecanismo mantém controles distintos para erros consecutivos e bloqueios.

Uma requisição válida zera o contador de erros consecutivos, mas não cancela um bloqueio ativo nem reinicia o histórico de penalidades acumuladas.

No cenário validado, a sequência de respostas é:

| Requisição | HTTP esperado |
|---|---|
| Primeira inválida | 400 |
| Segunda inválida | 400 |
| Requisição válida | 200 |
| Terceira inválida | 429 |

O histórico de bloqueios possui penalidades progressivas. Foram observados bloqueios de 5, 10, 15 minutos e durações superiores.

O término do tempo de bloqueio não implica o reinício do histórico acumulado.

Para permitir novas execuções em condições iniciais controladas, foi disponibilizada uma rota administrativa específica para liberação das penalidades.

### Cenários implementados

**Bloco 1 — Rate Limit em Atualizações**

Executa três requisições GET inválidas utilizando parâmetros fora dos limites aceitos.

Verifica HTTP 400 ou 429 e exige a ocorrência de pelo menos uma resposta de bloqueio.

Também valida o motivo do erro, a rota e os metadados associados ao bloqueio.

**Bloco 2 — Rate Limit em Revisão Fiscal**

Executa três requisições POST com EAN alfanumérico inválido.

Verifica as respostas HTTP e os metadados de bloqueio, incluindo o motivo relacionado ao EAN inválido.

**Bloco 3 — Contadores em Atualizações**

Executa uma requisição válida de preparação, seguida de duas requisições inválidas, uma válida e uma terceira inválida.

Valida a sequência de status HTTP 200, 400, 400, 200 e 429, considerando um CNPJ com os contadores inicialmente liberados.

**Bloco 4 — Contadores em Revisão Fiscal**

Aplica a mesma sequência de validação utilizando requisições POST e produtos válidos ou inválidos, conforme o cenário.

**Bloco 5 — Liberação do CNPJ**

Executa uma requisição POST para uma rota administrativa protegida, responsável pela liberação dos registros de penalidade e contagem associados ao CNPJ de teste.

O acesso utiliza autenticação Bearer, IP público e identificação do operador responsável pela execução.

Os Blocos 3 e 4 verificam o comportamento HTTP observado. Como os valores dos contadores internos não são expostos diretamente nas respostas desses endpoints, seus estados individuais não podem ser comprovados exclusivamente pelos status HTTP.

### Validações do HTTP 429

A função auxiliar `validar_resposta_bloqueio()` centraliza as validações dos campos comuns:

- `erro`
- `mensagem`
- `minutos_bloqueio`
- `aguardar_segundos`
- `bloqueio_iniciado_em`
- `liberado_em`

Os campos `motivo` e `rota` são validados individualmente nos respectivos testes.

Também é validada a presença do header `Retry-After` e sua correspondência com `aguardar_segundos`, considerando o primeiro valor quando o header apresenta valores separados por vírgula.

A duração informada pela API é comparada com o intervalo calculado entre `bloqueio_iniciado_em` e `liberado_em`.

### Execução controlada

**Os testes de Rate Limit não devem ser executados indiscriminadamente**, pois alteram o estado de bloqueio do CNPJ e podem aumentar progressivamente o tempo de penalidade.

A execução recomendada é realizada em uma bateria controlada.

Antes de uma bateria que dependa dos contadores inicialmente zerados, deve ser executado o Bloco 5.

Depois, os quatro testes devem ser executados na seguinte ordem:

1. Bloco 3 — Contadores em Atualizações.
2. Bloco 1 — Bloqueio em Atualizações.
3. Bloco 4 — Contadores em Revisão.
4. Bloco 2 — Bloqueio em Revisão.

Essa ordem permite aproveitar o bloqueio provocado pelos testes de contadores para validar os retornos HTTP 429.

**Não se deve liberar o CNPJ entre o Bloco 3 e o Bloco 1, nem entre o Bloco 4 e o Bloco 2**, pois a liberação removeria o estado que os testes seguintes precisam analisar.

### Executar os quatro testes de Rate Limit

Após executar a liberação administrativa, utilize:

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_reset_rate_limit_atualizacoes tests/test_v3_rate_limit.py::test_rate_limit_atualizacoes tests/test_v3_rate_limit.py::test_reset_rate_limit_revisao tests/test_v3_rate_limit.py::test_rate_limit_revisao -m rate_limit -v
```

Esse comando seleciona explicitamente os quatro testes na ordem definida, sem incluir o Bloco 5.

A execução conjunta pressupõe que o estado do CNPJ tenha sido preparado adequadamente e que não existam requisições concorrentes alterando os contadores.

### Execução individual dos testes

**Atualizações — Contadores**

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_reset_rate_limit_atualizacoes -m rate_limit -v
```

**Atualizações — Bloqueio**

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_rate_limit_atualizacoes -m rate_limit -v
```

**Revisão — Contadores**

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_reset_rate_limit_revisao -m rate_limit -v
```

**Revisão — Bloqueio**

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_rate_limit_revisao -m rate_limit -v
```

A execução individual deve respeitar as pré-condições de cada teste, especialmente o estado dos contadores e a existência de bloqueios ativos.

### Liberação do CNPJ entre execuções

**Antes de executar uma nova bateria de testes de Rate Limit que dependa dos contadores zerados, é obrigatório executar o Bloco 5.**

Isso acontece porque a API mantém o histórico de penalidades mesmo depois que o tempo de bloqueio termina.

Por exemplo, após três requisições inválidas, o CNPJ pode receber um bloqueio de 5 minutos.

Mesmo depois da liberação pelo tempo, uma nova requisição inválida poderá provocar outro bloqueio, agora de 10 minutos, em vez de retornar HTTP 400.

Esse comportamento interfere nos Blocos 3 e 4, que esperam uma sequência inicial de respostas HTTP 400, 400 e 429 para as requisições inválidas.

Para evitar falhas causadas pelo histórico acumulado, foi implementado o Bloco 5, que utiliza uma rota interna autorizada para remover registros de penalidade e contagem no Redis.

**Comando de liberação:**

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_liberacao_cnpj -m rate_limit -v
```

A requisição administrativa utiliza:

- **Método:** POST.
- **Rota:** `/v3.0/interno/penalidade/liberar/1/{CNPJ}/`.
- **Autorização:** header `Authorization` com Bearer Token.
- **`ip`:** endereço IP público obtido automaticamente.
- **`operador`:** identificação definida na variável `OPERADOR_RATE_LIMIT`.

A chave administrativa fica armazenada em `TOKEN_LIBERACAO_RATE_LIMIT`, no arquivo `.env`.

A rota deve ser utilizada exclusivamente para o CNPJ autorizado de QA.

O teste valida o retorno HTTP 200. No JSON, o campo `erro` informa o resultado da operação, e o objeto `liberado` apresenta a quantidade de chaves removidas para os controles de Revisão e Atualizações.

O retorno de zero chaves removidas pode indicar que não havia penalidade ou contagem registrada para os identificadores consultados.

**Fluxo recomendado:**

1. Executar o Bloco 5 para preparar o estado do CNPJ.
2. Executar a bateria dos quatro testes de Rate Limit.
3. Após a bateria, executar novamente o Bloco 5 antes de iniciar outra bateria que exija os contadores zerados.

A liberação administrativa deve ser realizada explicitamente, não sendo acionada automaticamente durante a regressão padrão.

### Cuidados importantes

- Utilizar exclusivamente credenciais autorizadas para os testes de Rate Limit.
- Não executar testes de bloqueio com o CNPJ da regressão padrão.
- Não executar a rota administrativa utilizando CNPJs de clientes reais sem autorização.
- Manter a chave Bearer administrativa exclusivamente no `.env` ou em armazenamento seguro de segredos.
- Configurar individualmente o nome do operador.
- Evitar execuções repetidas enquanto houver penalidades ativas.
- Não considerar uma requisição válida HTTP 200 como comprovação de término de bloqueio.
- Executar o Bloco 5 antes de uma nova bateria que exija contadores zerados.
- Não executar o Bloco 5 entre testes que dependam do bloqueio provocado pelo teste anterior.
- Considerar que a duração das penalidades pode aumentar progressivamente.
- Não utilizar `-m rate_limit` sozinho para executar indiscriminadamente todos os cenários, incluindo a liberação administrativa.
- Executar os testes de forma controlada e verificar os resultados antes de repetir uma bateria.

---

## Critérios de aceitação

A implementação do projeto contempla os seguintes critérios definidos para a suíte automatizada da API V3:

| Critério | Situação |
|---|---|
| Revisão Fiscal possui suíte automatizada | Atendido |
| Atualizações possui suíte automatizada | Atendido |
| Testes positivos e negativos estão implementados | Atendido |
| Limites de requisição estão cobertos | Atendido |
| Paginação está coberta | Atendido |
| Rate Limit está coberto separadamente | Atendido |
| Contrato da API V3 é representado a partir da documentação | Atendido |
| Campos, caminhos, hierarquias e tipos são comparados | Atendido |
| Campos não documentados são identificados | Atendido |
| Campos documentados não observados são identificados | Atendido |
| Divergências de tipo são identificadas | Atendido |
| Possíveis divergências de nome são sinalizadas | Atendido |
| Diferentes regimes tributários são analisados | Atendido |
| Relatório consolidado da validação de contrato é gerado | Atendido |
| Produto e regime são identificados nas divergências quando disponíveis | Atendido |
| Toda a regressão padrão pode ser executada por um comando | Atendido |
| É possível executar testes separados por endpoint | Atendido |
| É possível executar somente a validação de contrato | Atendido |
| É possível executar um teste individual | Atendido |
| Arquivo `.env` não está sendo rastreado pelo Git | Verificado |
| Cobertura da estrutura condicional `cargaliquida_cnae` | Pendente |
| Correção definitiva do comportamento de `filiais` | Pendente na API |
| README atualizado | Atendido |
| Projeto publicado no GitHub | Atendido |

Os critérios relacionados à cobertura representam os cenários implementados e executados na suíte, não uma garantia de que todos os comportamentos possíveis da API foram testados.

Os resultados registrados demonstram a execução da regressão e dos testes especiais nos cenários previstos.

---

## Repositório e reutilização pela equipe

O projeto está publicado no GitHub:

https://github.com/ferpedro04/testes-automatizados-v3

A suíte foi organizada para permitir que os integrantes da equipe executem a regressão completa, validem endpoints individualmente e acrescentem novos cenários conforme a evolução da API V3.

Os testes de Rate Limit possuem configurações e comandos específicos para evitar interferência na regressão padrão.

A validação de contrato permite identificar diferenças entre a documentação e a implementação atual, facilitando o registro de inconsistências e a verificação de correções realizadas pela equipe de desenvolvimento.

Após qualquer alteração relevante na API, recomenda-se executar a regressão automatizada e investigar eventuais falhas antes de considerar a mudança validada.

A documentação deve ser mantida atualizada conforme novas regras de negócio, endpoints e cenários sejam incorporados.

**O objetivo final é permitir que a equipe reutilize a suíte sempre que houver alterações na API V3, reduzindo a dependência de verificações manuais e facilitando a identificação de regressões e inconsistências de contrato.**