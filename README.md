# Suíte de Testes Automatizados — API V3.0 | Avant Fiscal

## Objetivo

Esta suíte de testes automatizados tem como objetivo validar o comportamento e os retornos das requisições realizadas aos endpoints da API V3.0 da Avant Fiscal:

- **POST `/revisao`** — Revisão Fiscal de produtos.
- **GET `/atualizacoes`** — Consulta de atualizações fiscais.

Os testes verificam o processamento das requisições, os status HTTP, os códigos de erro, as mensagens retornadas, a estrutura do JSON e as informações fiscais dos produtos.

A suíte contempla cenários positivos e negativos, incluindo validação de credenciais, parâmetros obrigatórios, dados tributários, limites de requisição, paginação e mecanismos de bloqueio por requisições inválidas.

O objetivo é identificar comportamentos inesperados, prevenir regressões após atualizações da API e contribuir para a confiabilidade dos serviços disponibilizados pela Avant Fiscal.

## Tecnologias utilizadas

- **Python** — Linguagem utilizada no desenvolvimento da suíte de testes.
- **Pytest** — Framework utilizado para criação e execução dos testes automatizados.
- **Requests** — Biblioteca utilizada para realizar requisições HTTP à API.
- **Python-dotenv** — Biblioteca utilizada para carregar as variáveis de ambiente armazenadas no arquivo `.env`.

## Estrutura do projeto

```text
projeto/
├── tests/
│   ├── conftest.py
│   ├── test_v3_revisao.py
│   ├── test_v3_atualizacao.py
│   └── test_v3_rate_limit.py
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
- **`.env`** — Armazena configurações e credenciais de acesso à API, incluindo as credenciais exclusivas de Rate Limit e a autorização administrativa. Não deve ser versionado.
- **`.env.example`** — Modelo das variáveis de ambiente necessárias para executar o projeto, sem credenciais reais.
- **`.gitignore`** — Define os arquivos e diretórios que não devem ser versionados.
- **`pytest.ini`** — Registra o marcador `rate_limit` e configura a exclusão desses testes da execução padrão.
- **`requirements.txt`** — Lista as dependências e versões utilizadas no projeto.
- **`README.md`** — Documenta a instalação, configuração, execução e manutenção da suíte.

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

## Organização dos testes

O projeto separa os testes de Revisão Fiscal, Atualizações e Rate Limit em arquivos diferentes.

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

## Executando os testes

Os testes são executados utilizando o **Pytest**, que identifica automaticamente arquivos e funções seguindo o padrão de nomenclatura `test_`.

### Executar toda a regressão padrão

```powershell
python -m pytest tests/ -v
```

Esse comando executa os testes de Revisão Fiscal e Atualizações, excluindo os testes de Rate Limit por meio da configuração do `pytest.ini`.

### Executar somente Revisão Fiscal

```powershell
python -m pytest tests/test_v3_revisao.py -v -s
```

### Executar somente Atualizações

```powershell
python -m pytest tests/test_v3_atualizacao.py -v -s -rs
```

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

### Opções utilizadas nos comandos

- **`-v`** — Exibe detalhadamente cada teste e seu resultado.
- **`-s`** — Permite visualizar as mensagens exibidas com `print()` durante a execução.
- **`-rs`** — Exibe os motivos dos testes marcados como `SKIPPED`.
- **`-m rate_limit`** — Seleciona os testes identificados pelo marcador `rate_limit`, sobrescrevendo a exclusão padrão configurada no projeto.
- **`--collect-only`** — Identifica e lista os testes sem executá-los.

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

Ao final da execução, o Pytest apresenta um resumo dos resultados.

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

Quando a API retorna a condição específica de ausência de atualizações necessárias ao cenário, os testes correspondentes utilizam `pytest.skip()`.

Essa estratégia evita que a suíte apresente falhas indevidas exclusivamente pela indisponibilidade de massa de dados.

O `skip` não deve ser utilizado para ocultar erros HTTP inesperados, problemas de autenticação ou falhas reais da API.

Os cenários que exigem massa de dados controlada poderão ser executados novamente quando houver um ambiente de homologação adequado.

## Resultado da regressão conjunta

Na execução conjunta realizada em 20/10/2026, foram registrados:

| Resultado | Quantidade |
|---|---:|
| Testes de regressão selecionados | 148 |
| PASSED | 141 |
| SKIPPED | 4 |
| XFAILED | 3 |
| FAILED inesperados | 0 |
| Testes de Rate Limit excluídos | 4 |

Os quatro testes pulados estavam relacionados à paginação sem massa de dados suficiente.

As três falhas esperadas estavam previamente identificadas na suíte de Revisão Fiscal.

Os quatro testes de Rate Limit foram excluídos da regressão, conforme a configuração de isolamento.

Esse resultado corresponde à execução registrada nessa data e pode variar conforme alterações posteriores no código, na API e nos dados disponíveis.

## Cuidados para manutenção

Ao adicionar novos testes ao projeto:

- Manter cenários de Revisão, Atualizações e Rate Limit em seus respectivos arquivos.
- Centralizar configurações e credenciais nas fixtures apropriadas e no `.env`.
- Evitar incluir credenciais reais diretamente no código.
- Reutilizar respostas armazenadas no cache quando os cenários utilizarem a mesma requisição.
- Preservar testes independentes e executáveis individualmente sempre que possível.
- Verificar o comportamento esperado na API antes de definir os asserts.
- Não utilizar `pytest.skip()` para esconder defeitos reais.
- Executar a regressão completa após alterações significativas na suíte.
- Evitar executar testes que provocam bloqueios utilizando credenciais da regressão padrão.
- Não incluir a chave de autorização administrativa no código-fonte ou no repositório.

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

Executa três requisições GET inválidas utilizando parâmetros fora dos limites aceitos. Verifica HTTP 400 ou 429 e exige a ocorrência de pelo menos uma resposta de bloqueio.

Também valida o motivo do erro, a rota e os metadados associados ao bloqueio.

**Bloco 2 — Rate Limit em Revisão Fiscal**

Executa três requisições POST com EAN alfanumérico inválido. Verifica as respostas HTTP e os metadados de bloqueio, incluindo o motivo relacionado ao EAN inválido.

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

Por exemplo, após três requisições inválidas, o CNPJ pode receber um bloqueio de 5 minutos. Mesmo depois da liberação pelo tempo, uma nova requisição inválida poderá provocar outro bloqueio, agora de 10 minutos, em vez de retornar HTTP 400.

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

### Resultado da execução dos testes de Rate Limit

Na execução conjunta realizada em 20/10/2026, foram registrados:

| Resultado | Quantidade |
|---|---:|
| Testes de Rate Limit executados | 4 |
| PASSED | 4 |
| FAILED | 0 |

**Tempo de execução:** 19,99 segundos.

Os quatro testes foram executados na ordem controlada, após a preparação do CNPJ, com todas as validações aprovadas.

O Bloco 5 também foi executado individualmente e retornou HTTP 200.

Esses resultados correspondem às execuções registradas nessa data e podem variar conforme alterações posteriores no código, na API e no estado dos contadores.

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