# projeto-basic-rest-api

Criação das operações básicas do acrônimo CRUD através de uma séria de Rest API's para manipular um dicionário, que contém uma lista de livros clássicos da
literatura brasileira.

Configuração do ambiente:

Python 3.10.12

Checar se a biblioteca 'virtualenv' está instalada:
pip list

Instalar caso não esteja presente na saída anterior:
pip install virtualenv

python3 -m venv basic_api_project

source basic_api_project/bin/activate

pip install flask flask-restful

caso alguma importação dê erro, checar se o interpretador python usado é o coprreto (o do ambiente virtual deve ser usado)

CTRL + SHIFT + P
Python: Select Interpreter

Selecionar
.venv/bin/python
ou
.venv\Scripts\python.exe (no Windows)

deactivate