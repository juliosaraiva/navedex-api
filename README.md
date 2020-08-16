# NAVEDEX's Project

## Navedex API

---

### O sistema:

Este sistema consiste em um criador de navedex's, para o desafio de código referente a vaga de desenvolvedor backend python/django na Nave.rs.

### Resumo das funcionalidades:

- Autenticação
  - (Singup) Rota de cadastro através de email e senha no body da requisição no formato JSON.
  - (Login) Rota para login no sistema deve ser enviado e-mail e senha no formato JSON no body da requisição e será retornado um JSON com o email do usuário logado e o token contendo o refresh e access.

> As demais rotas da aplicação são acessadas somente se o usuário estiver autenticado com o token sendo passado no header da requisição.

- Navers

  - A rota (Index) possui os filtros por nome, tempo de empresa e cargo conforme requisito e retornando um array.
  - Somente é retornado os navers que pertence ao usuário que o cadastrou
  - A rota (Show) detalha as informações de um naver incluindo os projetos que ele está participando.
  - Também é possível atualizar um naver através dos métodos PATCH ou PUT e remover através do DELETE

- PROJECTS
  - A rota (index) possui filtros por nome que retorna exatamente o projeto passado no query_param.
  - Somente é retornado os projetos que pertence ao usuário que o cadastrou.
  - A rota (show) detalha as informações de um projeto, incluindo os navers que estão participando do projeto.
  - Também é possível atualizar um projeto através dos métodos PATCH ou PUT e remover através do DELETE

# Setup do Projeto

Os passos seguintes descrevem a configuração do projeto.

Copiar o arquivo `contrib/.env-sample` para a raiz do projeto, renomeando-o para `.env`.

Criar um venv com o pipenv

```sh
$ python -m pip install pipenv

$ PIPENV_VENV_IN_PROJECT=1

$ pipenv --python 3.8

$ pipenv sync
```

> No powershell, para criar a variavel de ambiente pode-se usar o seguinte comando:

```powershell
$set:PIPENV_VENV_IN_PROJECT=1
```

Gerar um `SECRET_KEY` para adicionar no arquivo `.env`.

```sh
$ pipenv run python commands/generate_secret.py
```

Rodar os testes e o projeto

```sh
$ cd src/
$ pipenv run python manage.py test
$ pipenv run python manage.py runserver
```

- No diretorio contrib, contem o arquivo do `INSOMNIA`, para realizar os testes na API.
- Ao importar os dados no Insomnia, pode-se pressionar Ctrl + E, para obter a lista de variaveis definidas usadas nos testes.
