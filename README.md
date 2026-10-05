## Objetivo

Esta suíte de testes automatizados tem como objetivo validar o retorno das requisições realizadas ao endpoint de Revisão Fiscal da API V3.0 da Avant Fiscal.

Os testes verificam se a requisição é processada com sucesso (`erro = 0`), além de validar a quantidade de produtos enviados e encontrados, as principais informações dos produtos retornados e seus respectivos dados tributários.

A suíte contempla cenários de revisão com um único produto e com múltiplos produtos.

## Tecnologias utilizadas

- **Python** - Linguagem utilizada no desenvolvimento da suíte de testes.
- **Pytest** - Framework utilizado para criação e execução dos testes automatizados.
- **Requests** - Biblioteca utilizada para realizar as requisições HTTP para a API.
- **Python-dotenv** - Biblioteca utilizada para carregar as variáveis de ambiente armazenadas no arquivo `.env`.

## Estrutura do projeto
projeto/
├── tests/
│   ├── conftest.py
│   └── test_v3_revisao.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

- **tests/conftest.py** - Centraliza as configurações, os dados de teste e as fixtures utilizadas pelos testes.
- **tests/test_v3_revisao.py** - Contém os cenários de teste e as validações realizadas sobre as respostas da API.
- **`.env`** - Armazena as variáveis de ambiente utilizadas pela suíte, incluindo configurações e credenciais de acesso à API. Este arquivo contém informações sensíveis e não deve ser versionado.
- **`.env.example`** - Modelo das variáveis de ambiente necessárias para executar o projeto. Serve como referência para que, ao clonar o repositório, seja possível criar e preencher corretamente o arquivo `.env` sem expor credenciais reais.
- **`.gitignore`** - Define arquivos e diretórios que não devem ser versionados pelo Git, evitando o envio de informações sensíveis e arquivos gerados localmente que não são necessários no repositório.
- **`requirements.txt`** - Lista as dependências e versões necessárias para executar o projeto, permitindo que sejam instaladas de uma vez através do `pip`.

## Instalação e configuração

### 1. Criar e ativar o ambiente virtual

O ambiente virtual (`venv`) cria um espaço isolado para as dependências do projeto. Dessa forma, as bibliotecas utilizadas pela suíte de testes são instaladas somente nesse ambiente, evitando conflitos com outros projetos ou com a instalação global do Python.

Para criar o ambiente virtual, rode no terminal:
python -m venv venv
E após isso, para ativá-lô, use o comando:
.\venv\Scripts\Activate.ps1

### 2. Instalar as dependências
Com o ambiente virtual ativo, instale as bibliotecas necessárias para executar a suíte:
pip install -r requirements.txt
O arquivo requirements.txt contém as dependências e suas respectivas versões, garantindo que o ambiente utilizado para executar os testes possua as bibliotecas necessárias.

### 3. Configurar as variáveis de ambiente
O projeto utiliza um arquivo `.env` para armazenar configurações e credenciais utilizadas nos testes.
Essas informações ficam separadas do código para evitar a exposição de dados sensíveis no repositório.
O arquivo `.env.example` contém o modelo das variáveis necessárias. Após clonar o projeto, crie um arquivo chamado `.env` na raiz e preencha os valores correspondentes.

Exemplo:
env
URL_BASE=
ID_PARCEIRO=
CNPJ=
TOKEN=
CMUN=
REGIME=
CRT=

## Executando os testes

Os testes são executados utilizando o **Pytest**. Ele identifica automaticamente os arquivos e funções de teste seguindo o padrão de nomenclatura `test_`.

### Executar toda a suíte

Para executar todos os testes do projeto:

pytest -v


A opção `-v` (verbose) exibe de forma detalhada cada teste executado e seu respectivo resultado.

### Executar apenas os testes da API V3

Para executar todos os testes presentes no arquivo `test_v3_revisao.py`:

pytest -v tests/test_v3_revisao.py


### Executar um teste específico

É possível executar apenas um cenário utilizando o nome da função:

pytest -v tests/test_v3_revisao.py::test_quantidade_multiplos_produtos


### Executar testes específicos em conjunto

Também é possível selecionar mais de um teste na mesma execução:

pytest -v tests/test_v3_revisao.py::test_encontrados_multiplos_produtos tests/test_v3_revisao.py::test_quantidade_multiplos_produtos


## Entendendo os resultados

Cada teste utiliza `assert` para validar se o comportamento retornado pela API corresponde ao comportamento esperado.

Exemplo:

python
assert response.status_code == 200
Nesse caso, o teste verifica se a API retornou o status HTTP `200`.

Ao executar a suíte, o Pytest informa individualmente o resultado dos testes:

- `PASSED` - A validação foi realizada com sucesso.
- `FAILED` - O resultado obtido foi diferente do esperado pela validação.

Ao final da execução, também é apresentado um resumo com a quantidade total de testes aprovados e reprovados.

## Cenários validados

A suíte contempla cenários de sucesso do endpoint de Revisão Fiscal da API V3.0, incluindo:

- Requisição com credenciais válidas;
- Revisão com um produto válido;
- Revisão com múltiplos produtos válidos;
- Status HTTP de sucesso;
- Retorno de `erro = 0`;
- Quantidade de produtos enviados;
- Quantidade de produtos encontrados;
- Existência do array `itens`;
- Quantidade de itens retornados;
- Informações principais dos produtos;
- Informações tributárias dos produtos;
- Retorno de `regime_tributario`;
- Retorno de `crt`;
- Retorno de `cMun`;
- Validação das informações principais de todos os produtos em uma requisição múltipla;
- Validação das informações tributárias de todos os produtos em uma requisição múltipla.