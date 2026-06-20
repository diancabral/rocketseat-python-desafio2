# Rocketseat Python — Desafio 2

API REST em **Flask** para gestão de **usuários** e **refeições** (cadastro, login com sessão, CRUD de refeições com regras de acesso), com **MySQL**, **SQLAlchemy**, **Alembic**, **Pydantic** para validação de payloads e **Flask-Login** para autenticação baseada em **cookie de sessão**.

**Prefixo base da API:** `/api`

---

## Requisitos

- **Python** `>= 3.12.10`
- **[uv](https://docs.astral.sh/uv/)** (gerenciador de dependências e ambiente virtual)
- **Docker** e **Docker Compose** (para subir o MySQL localmente)

---

## Configuração do ambiente

### 1. Clonar o repositório e entrar na pasta

```bash
git clone <url-do-repositório>
cd rocketseat-python-desafio2
```

### 2. Variáveis de ambiente

Copie o exemplo e ajuste os valores (principalmente `SECRET_KEY` e a URI do banco):

```bash
cp .env.example .env
```

| Variável | Descrição |
|----------|-----------|
| `SECRET_KEY` | Chave secreta do Flask (sessões e cookies assinados). Use um valor forte em produção. |
| `SQLALCHEMY_DATABASE_URI` | URI SQLAlchemy para MySQL, ex.: `mysql+pymysql://USUARIO:SENHA@127.0.0.1:3306/NOME_DO_BANCO` |
| `MYSQL_ROOT_PASSWORD` | Senha do usuário `root` no container MySQL |
| `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_DATABASE` | Usuário, senha e nome do banco criados pelo Compose |

**Importante:** o usuário e o banco em `SQLALCHEMY_DATABASE_URI` precisam existir e bater com o que o MySQL do Docker está configurado a criar (via `MYSQL_*`). Por exemplo, se no `.env` do Compose você usa `MYSQL_USER=user`, a URI pode usar esse usuário (e a senha `MYSQL_PASSWORD`) ou `root` com `MYSQL_ROOT_PASSWORD`.

### 3. Banco de dados (MySQL via Docker)

```bash
make db-up
```

Aguarde o MySQL ficar pronto (alguns segundos na primeira subida).

### 4. Dependências Python

```bash
make install
```

Equivale a `uv sync`, criando/atualizando o ambiente em `.venv`.

### 5. Migrations (Alembic)

Aplicar o schema atual no banco:

```bash
make alembic-upgrade
```

Para gerar uma nova revisão após mudar modelos (com mensagem customizada):

```bash
make alembic-revision MSG="descrição da mudança"
```

---

## Executar a API

```bash
make run
```

Por padrão o Flask sobe em modo debug em **http://127.0.0.1:5000/**.

Outros alvos úteis do `Makefile`:

| Comando | Descrição |
|---------|-----------|
| `make help` | Lista os comandos disponíveis |
| `make flask-shell` | Shell Flask com `PYTHONPATH=src` |
| `make db-down` | Para os containers do Compose |
| `make db-logs` | Acompanha logs do serviço `db` |
| `make clean` | Remove `__pycache__` e `.pyc` |

---

## Autenticação

A API usa **Flask-Login** com **sessão em cookie** (`Set-Cookie` após login).

- Rotas marcadas com `@login_required` exigem sessão válida.
- Sem sessão (ou sessão inválida): resposta **401** com código `UNAUTHORIZED`.
- Logado, mas sem permissão para o recurso (ex.: outro usuário que não seja admin): **403** com código `FORBIDDEN`.

**Dica com `curl`:** use `-c cookies.txt` no login e `-b cookies.txt` nas requisições seguintes para reutilizar o cookie de sessão.

---

## Formato das respostas

- Respostas JSON costumam incluir o campo `code` (string identificando o resultado de negócio) e, quando aplicável, `message` ou outros campos (objetos, listas, etc.).
- Erros de validação Pydantic retornam **422** com `code: "VALIDATION_ERROR"` e lista `errors` com `field`, `message` e `type`.

---

## Endpoints

Todas as URLs abaixo assumem base `http://127.0.0.1:5000`.

### Health

| Método | Caminho | Autenticação | Descrição |
|--------|---------|--------------|-----------|
| `GET` | `/api/health/` | Não | Verificação de saúde da API (`code` de sucesso configurado no módulo health). |

### Usuários

| Método | Caminho | Autenticação | Descrição |
|--------|---------|--------------|-----------|
| `POST` | `/api/v1/users/` | Não | Cria usuário. Corpo JSON abaixo. |
| `GET` | `/api/v1/users/me/` | Sim | Retorna o usuário logado (`uuid`, `username`, `email`, `role`). |

**`POST /api/v1/users/` — corpo (JSON)**

```json
{
  "username": "string, máx. 24",
  "password": "string, máx. 24",
  "email": "e-mail válido"
}
```

- Sucesso: mensagem de criação e código `USER_CREATED`.
- Username duplicado: **409** e `USER_ALREADY_EXISTS`.

### Autenticação

| Método | Caminho | Autenticação | Descrição |
|--------|---------|--------------|-----------|
| `POST` | `/api/v1/auth/login/` | Não | Login; em sucesso, define cookie de sessão. |
| `GET` | `/api/v1/auth/logout/` | Sim | Encerra a sessão. |

**`POST /api/v1/auth/login/` — corpo (JSON)**

```json
{
  "username": "string, máx. 24",
  "password": "string, máx. 24"
}
```

- Sucesso: `AUTH_LOGIN_SUCCESS`.
- Credenciais inválidas: **401**, `AUTH_LOGIN_ERROR`.

### Refeições

Regras de acesso:

- O **dono** da refeição (`user_id`) pode ver/editar/excluir e listar suas refeições.
- Usuário com **`role` igual a `admin`** pode as mesmas operações em refeições de qualquer usuário e listar refeições de qualquer `user_id`.

| Método | Caminho | Autenticação | Descrição |
|--------|---------|--------------|-----------|
| `POST` | `/api/v1/meals/` | Sim | Cria refeição para o **usuário logado**. |
| `GET` | `/api/v1/meals/<uuid>` | Sim | Detalhe de uma refeição (com dados resumidos do usuário). |
| `PATCH` | `/api/v1/meals/<uuid>` | Sim | Atualização parcial. |
| `DELETE` | `/api/v1/meals/<uuid>` | Sim | Remove a refeição. |
| `GET` | `/api/v1/meals/user/<uuid>` | Sim | Lista refeições do usuário informado. |

**`POST /api/v1/meals/` — corpo (JSON)**

```json
{
  "name": "string, máx. 24",
  "description": "string, máx. 100",
  "is_diet": true
}
```

**`PATCH /api/v1/meals/<uuid>` — corpo (JSON)**  
Campos opcionais; envie apenas o que deseja alterar. Campos extras não permitidos (`extra: forbid` no schema).

```json
{
  "name": "opcional",
  "description": "opcional",
  "is_diet": true
}
```

- Códigos úteis: `MEAL_CREATED`, `MEAL_UPDATED`, `MEAL_NOT_UPDATED`, `MEAL_DELETED`, `MEAL_NOT_FOUND`.
- Refeição inexistente: **404** com `MEAL_NOT_FOUND`.
- Lista vazia em `GET .../meals/user/<uuid>`: **204** com `meals: []`.

---

## Exemplo rápido com `curl`

Substitua usuário, senha e URLs conforme seu ambiente.

```bash
# 1) Criar usuário
curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"joao","password":"senha123456789","email":"joao@example.com"}'

# 2) Login (guarda cookies)
curl -s -c cookies.txt -X POST http://127.0.0.1:5000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"joao","password":"senha123456789"}'

# 3) Perfil logado
curl -s -b cookies.txt http://127.0.0.1:5000/api/v1/users/me/

# 4) Criar refeição
curl -s -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/meals/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Almoço","description":"Arroz e feijão","is_diet":true}'

# 5) Listar refeições do usuário (troque <UUID_DO_USUARIO> pelo retornado em /me/)
curl -s -b cookies.txt http://127.0.0.1:5000/api/v1/meals/user/<UUID_DO_USUARIO>/
```

---

## Estrutura do projeto (resumo)

- `src/app.py` — ponto de entrada (`create_app()` e `app.run(debug=True)` em modo direto).
- `src/config/` — fábrica da app, rotas, banco, constantes.
- `src/models/` — modelos SQLAlchemy (`User`, `Meals`) e utilitários (ex.: tipo UUID).
- `src/modules/` — blueprints por domínio (`auth`, `users`, `meals`, `health`).
- `src/utils/` — `http_response`, tratamento de validação e erros HTTP.
- `alembic/` — migrations; `alembic.ini` na raiz.

---

## Papéis (`role`)

- Novos usuários criados pela API recebem `role` **`user`** por padrão.
- Usuários com `role` **`admin`** têm acesso ampliado às rotas de refeições (conforme descrito acima). Para ter um admin no banco, é preciso ajustar o registro diretamente no MySQL ou via ferramenta de sua escolha (não há endpoint público de promoção a admin neste projeto).

---

## Problemas comuns

| Sintoma | O que verificar |
|---------|-----------------|
| Erro ao conectar no MySQL | Container ativo (`make db-up`), porta `3306` livre, URI em `SQLALCHEMY_DATABASE_URI` com usuário/senha/banco corretos. |
| `SECRET_KEY` / `SQLALCHEMY_DATABASE_URI` ausentes | Arquivo `.env` na **raiz** do projeto (o código carrega a partir daí). |
| 401 em rotas protegidas | Login feito com sucesso e cookie enviado (`-b cookies.txt` no `curl` ou equivalente no cliente). |
| Tabelas inexistentes | Rodar `make alembic-upgrade` após o banco estar no ar. |