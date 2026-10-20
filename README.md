# Suíte de Testes Automatizados — API V3.0 | Avant Fiscal

## Objetivo

Esta suíte de testes automatizados tem como objetivo validar o comportamento e os retornos das requisições realizadas aos endpoints da API V3.0 da Avant Fiscal:

- **POST `/revisao`** — Revisão Fiscal de produtos.
- **GET `/atualizacoes`** — Consulta de atualizações fiscais.

Os testes verificam o processamento das requisições, os status HTTP, os códigos de erro, as mensagens retornadas, a estrutura do JSON e as informações fiscais dos produtos.

A suíte contempla cenários positivos e negativos, incluindo validação de credenciais, parâmetros obrigatórios, dados tributários, limites de requisição e paginação.

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
- **`tests/test_v3_rate_limit.py`** — Contém os testes específicos do mecanismo de bloqueio dos endpoints de Revisão e Atualizações, separados da regressão padrão.
- **`.env`** — Armazena configurações e credenciais de acesso à API, incluindo as credenciais exclusivas de Rate Limit. Não deve ser versionado.
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
```

Preencha os valores correspondentes ao ambiente de testes autorizado.

**Importante:** o arquivo `.env` contém credenciais e não deve ser enviado ao GitHub ou compartilhado publicamente.

## Organização dos testes

O projeto separa os testes de Revisão Fiscal e de Atualizações em arquivos diferentes.

As configurações e fixtures compartilhadas são centralizadas em `conftest.py`, facilitando a reutilização dos dados e a manutenção da suíte.

### Isolamento dos testes de Rate Limit

Os testes de Rate Limit são mantidos em `tests/test_v3_rate_limit.py` e identificados pelo marcador `pytest.mark.rate_limit`.

O arquivo `pytest.ini` utiliza a configuração `addopts = -m "not rate_limit"` para excluir esses testes da regressão padrão.

O objetivo é impedir que a execução habitual da suíte provoque bloqueios temporários no CNPJ utilizado nos testes de Revisão Fiscal e Atualizações.

As requisições de Rate Limit utilizam credenciais específicas, carregadas pelas variáveis `CNPJ_RATE_LIMIT` e `TOKEN_RATE_LIMIT`.

Diferentemente das validações de regressão que reutilizam respostas em cache, os testes de Rate Limit realizam requisições HTTP reais e consecutivas, pois precisam observar o comportamento do mecanismo de bloqueio.

### Reutilização de requisições

A suíte utiliza uma fixture de cache para armazenar respostas HTTP e reutilizá-las entre testes que compartilham o mesmo cenário.

Esse mecanismo evita requisições repetidas desnecessariamente, especialmente quando diferentes testes validam o status HTTP, o código de erro e a mensagem de uma mesma resposta.

Cada cenário utiliza uma chave própria no cache, evitando misturar respostas de requisições diferentes.

O cache funciona durante a execução configurada da suíte e não representa armazenamento permanente entre execuções independentes.

## Executando os testes

Os testes são executados utilizando o **Pytest**, que identifica automaticamente arquivos e funções seguindo o padrão de nomenclatura `test_`.

### Executar toda a suíte

```powershell
python -m pytest tests/ -v
```

Esse comando executa os testes de Revisão Fiscal e Atualizações.

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

Na execução conjunta realizada em 15/10/2026, foram registrados:

| Resultado | Quantidade |
|---|---:|
| Testes coletados | 148 |
| PASSED | 141 |
| SKIPPED | 4 |
| XFAILED | 3 |
| FAILED inesperados | 0 |

**Tempo de execução:** 138,11 segundos.

Os quatro testes pulados estavam relacionados à paginação sem massa de dados suficiente.

As três falhas esperadas estavam previamente identificadas na suíte de Revisão Fiscal.

Esse resultado corresponde à execução registrada nessa data e pode variar conforme alterações posteriores no código, na API e nos dados disponíveis.

## Cuidados para manutenção

Ao adicionar novos testes ao projeto:

- Manter cenários de Revisão e Atualizações em seus respectivos arquivos.
- Centralizar configurações e credenciais nas fixtures apropriadas e no `.env`.
- Evitar incluir credenciais reais diretamente no código.
- Reutilizar respostas armazenadas no cache quando os cenários utilizarem a mesma requisição.
- Preservar testes independentes e executáveis individualmente.
- Verificar o comportamento esperado na API antes de definir os asserts.
- Não utilizar `pytest.skip()` para esconder defeitos reais.
- Executar a regressão completa após alterações significativas na suíte.

## Testes de Rate Limit — API V3

O Rate Limit é um mecanismo de proteção da API que controla requisições inválidas e aplica bloqueios temporários quando determinadas condições são atingidas.

A suíte automatizada contempla os endpoints:

- **POST `/revisao`**
- **GET `/atualizacoes`**

### Comportamento do mecanismo

Conforme as regras confirmadas com o desenvolvedor responsável, o mecanismo mantém controles distintos para erros consecutivos e bloqueios.

Uma requisição válida zera o contador de erros consecutivos, mas não cancela um bloqueio ativo nem necessariamente reinicia o histórico de penalidades.

No cenário validado, a sequência de respostas é:

| Requisição | HTTP esperado |
|---|---|
| Primeira inválida | 400 |
| Segunda inválida | 400 |
| Requisição válida | 200 |
| Terceira inválida | 429 |

O histórico de bloqueios possui penalidades progressivas. Foram observados bloqueios de 5, 10, 15 minutos e durações superiores.

A política de expiração ou reinicialização desse histórico ainda precisa ser esclarecida.

### Cenários implementados

**Bloco 1 — Rate Limit em Atualizações**

Executa três requisições GET inválidas utilizando parâmetros fora dos limites aceitos. Verifica HTTP 400 ou 429 e exige a ocorrência de pelo menos uma resposta de bloqueio.

**Bloco 2 — Rate Limit em Revisão Fiscal**

Executa três requisições POST com EAN alfanumérico inválido. Verifica as respostas e os metadados de bloqueio.

**Bloco 3 — Contadores em Atualizações**

Valida a sequência de requisições inválidas e válidas, incluindo o HTTP 429 na terceira tentativa inválida contabilizada para bloqueio.

**Bloco 4 — Contadores em Revisão Fiscal**

Aplica a mesma sequência de validação utilizando requisições POST.

Os Blocos 3 e 4 verificam o comportamento HTTP observado. Como os contadores internos não são expostos nas respostas, não é possível comprovar diretamente seus valores somente com esses testes.

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

### Execução controlada

**Os testes de Rate Limit não devem ser executados indiscriminadamente**, pois alteram temporariamente o estado de bloqueio do CNPJ.

A execução recomendada é realizada por endpoint, em pares:

1. Executar o teste de contadores em um ambiente sem bloqueio ativo.
2. Aproveitar o bloqueio provocado para executar o teste de resposta HTTP 429.
3. Respeitar o período de liberação antes de iniciar outro cenário que dependa de um estado desbloqueado.

#### Atualizações — Teste dos contadores

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_reset_rate_limit_atualizacoes -m rate_limit -v -s
```

#### Atualizações — Validação do bloqueio

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_rate_limit_atualizacoes -m rate_limit -v -s
```

#### Revisão — Teste dos contadores

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_reset_rate_limit_revisao -m rate_limit -v -s
```

#### Revisão — Validação do bloqueio

```powershell
python -m pytest tests/test_v3_rate_limit.py::test_rate_limit_revisao -m rate_limit -v -s
```

### Cuidados importantes

- Utilizar exclusivamente credenciais autorizadas para os testes de Rate Limit.
- Não executar testes de bloqueio com o CNPJ da regressão padrão.
- Evitar execuções repetidas enquanto houver penalidades ativas.
- Não considerar uma requisição válida HTTP 200 como comprovação de término de bloqueio.
- Executar os testes de contadores apenas em condições iniciais adequadas.
- Considerar que a duração das penalidades pode aumentar progressivamente.
- Não executar os quatro testes em sequência sem controlar as pré-condições de cada endpoint.
- Não utilizar o marcador `rate_limit` indiscriminadamente para executar todos os cenários em conjunto.