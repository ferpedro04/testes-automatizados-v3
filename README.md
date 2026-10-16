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
│   └── test_v3_atualizacao.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

- **`tests/conftest.py`** — Centraliza configurações, dados de teste e fixtures reutilizadas pelas suítes.
- **`tests/test_v3_revisao.py`** — Contém os cenários positivos e negativos do endpoint de Revisão Fiscal.
- **`tests/test_v3_atualizacao.py`** — Contém os cenários positivos e negativos do endpoint de Atualizações, incluindo paginação e limites.
- **`.env`** — Armazena as configurações e credenciais utilizadas nos testes. Contém informações sensíveis e não deve ser versionado.
- **`.env.example`** — Modelo das variáveis de ambiente necessárias para executar o projeto, sem expor credenciais reais.
- **`.gitignore`** — Define os arquivos e diretórios que não devem ser versionados pelo Git.
- **`requirements.txt`** — Lista as dependências e respectivas versões necessárias para executar o projeto.
- **`README.md`** — Documentação de instalação, configuração, execução e organização da suíte.

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
```

Preencha os valores correspondentes ao ambiente de testes autorizado.

**Importante:** o arquivo `.env` contém credenciais e não deve ser enviado ao GitHub ou compartilhado publicamente.

## Organização dos testes

O projeto separa os testes de Revisão Fiscal e de Atualizações em arquivos diferentes.

As configurações e fixtures compartilhadas são centralizadas em `conftest.py`, facilitando a reutilização dos dados e a manutenção da suíte.

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

## Próxima etapa — Testes de Rate Limit

O projeto será expandido para incluir testes específicos do mecanismo de bloqueio dos endpoints de Revisão Fiscal e Atualizações.

Essa etapa contemplará erros consecutivos, HTTP 429, header `Retry-After`, metadados de bloqueio e reinicialização do contador após uma requisição válida.

**Os testes de Rate Limit deverão ficar isolados da regressão padrão**, pois podem provocar o bloqueio temporário das credenciais utilizadas nas consultas.

A implementação, os comandos de execução e as configurações específicas serão documentados após a conclusão dessa etapa.