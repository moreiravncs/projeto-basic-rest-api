# Implementação de REST API com autenticação básica

## Descrição

Este projeto implementa as operações básicas de uma API RESTful, cobrindo o ciclo CRUD (Create, Read, Update, Delete) para uma lista de livros clássicos da literatura brasileira. Os dados são armazenados em um dicionário Python, simulando uma base de dados em memória.

Um dos endpoints é protegido com autenticação básica (Basic Auth).

---

## Tecnologias utilizadas

- Flask — framework web minimalista em Python  
- Flask-RESTful — extensão para facilitar a criação de APIs RESTful  
- Postman — utilizado para testar os endpoints da API  

---

## Configuração do ambiente

Este projeto foi desenvolvido em Ubuntu (WSL), mas funciona em qualquer sistema com Python instalado.

```bash
# Instalar o virtualenv, se ainda não tiver:
pip install virtualenv

# Criar o ambiente virtual:
python3 -m venv basic_api_project

# Ativar o ambiente virtual:
source basic_api_project/bin/activate  # Linux/macOS
# venv\Scripts\activate                # Windows

# Instalar as dependências:
pip install -r requirements.txt
```

Caso alguma importação falhe, verifique se o interpretador Python correto está sendo usado (no VS Code: `Ctrl+Shift+P` → "Python: Select Interpreter" → selecione o da venv).

---

## Estrutura do projeto

- `books_api.py`: Arquivo principal que define os recursos da API e as rotas  
- `config.py`: Contém as credenciais usadas na autenticação (não está versionado)  
- `books_data.py`: Simula um banco de dados com os livros  
- `requirements.txt`: Lista de dependências  

---

## Como funciona

1. O decorador `login_required` intercepta chamadas para checar credenciais. Ele protege o endpoint `GET /books/<book_id>`.

2. O `RequestParser` valida os dados enviados no `POST` e `PUT`.

3. A classe `Book` manipula registros individuais (`GET`, `PUT`, `DELETE` com `book_id`).

4. A classe `BookList` gerencia a coleção de livros (`GET` para listar todos, `POST` para adicionar um novo).

5. Ambas as classes são registradas como recursos via `api.add_resource`.

---

## Pontos de melhoria

- [ ] Persistência com banco de dados (SQLite, PostgreSQL, etc.)
- [ ] Testes unitários com `unittest` ou `pytest`
- [ ] Tratamento de exceções e mensagens de erro mais claras
- [ ] Dockerização do projeto
- [ ] Uso de frameworks mais modernos, como `Flask-Smorest` ou `FastAPI`
