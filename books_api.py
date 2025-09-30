from flask_restful import Api, Resource, abort, reqparse
from flask import Flask, request, make_response
from functools import wraps
from config import USERNAME, PASSWORD

# entrypoint para a aplicação Flask
app = Flask(__name__)

# entrypoint da aplicação para o Flask Restful
api = Api(app)

BOOKS = {
    'book_1': {'title': 'Dom Casmurro', 'author': 'Machado de Assis'},
    'book_2': {'title': 'O Guarani', 'author': 'José de Alencar'},
    'book_3': {'title': 'Memórias Póstumas de Brás Cubas', 'author': 'Machado de Assis'},
    'book_4': {'title': 'Iracema', 'author': 'José de Alencar'},
    'book_5': {'title': 'O Cortiço', 'author': 'Aluísio Azevedo'},
    'book_6': {'title': 'A Moreninha', 'author': 'Joaquim Manuel de Macedo'},
    'book_7': {'title': 'Capitães da Areia', 'author': 'Jorge Amado'},
    'book_8': {'title': 'Senhora', 'author': 'José de Alencar'},
    'book_9': {'title': 'Vidas Secas', 'author': 'Graciliano Ramos'},
    'book_10': {'title': 'Grande Sertão: Veredas', 'author': 'João Guimarães Rosa'}
}

# função que recebe função como argumento (event)
# event é a função que será decorada
def login_required(event):
    
    # o decorador wraps preserva a função a ser decorada (sem ele o nome dela passaria a ser login)
    @wraps(event)
    def login(*args, **kwargs):
        '''
            Essa função intercepta a chamada original, checa as credenciais
            e decide se a função será executada ou não.
            *args e **kwargs ´r porque a assinatura da função decorada é desconhecida.
        '''
        
        # verifica se possui cabeçalho de autenticação e se as credenciais estão corretas
        if request.authorization and  \
        request.authorization.username == USERNAME and\
        request.authorization.password == PASSWORD:
            return event(*args, **kwargs)
        
        # {'WWW-Authenticate': 'Basic realm="Login Realm"'} é especificação oficial para autenticação básica do HTTP (abre um popup)
        return make_response('Could not verify your credentials',
                             401,
                             {'WWW-Authenticate': 'Basic realm="Login Realm"'})
    
    return login

# RequestParser cria um "validador" de argumentos da requisição
parser = reqparse.RequestParser()
        
# campos esperados na requisição
parser.add_argument('title')
parser.add_argument('author')

"""
    'Resource' é uma classe abstrata, a implementação concreta dela
    deve herdar da mesma e expor os métodos http.
    
    Não é possível que uma mesma classe do tipo 'Resource' possua dois métodos 'get', por exemplo. E isso se aplica aos demais métodos http.
"""

class BookList(Resource):
    def get(self):
        return BOOKS
    
    def post(self):
        args = parser.parse_args()
        
        current_book_id = 0
        
        # Garantindo que o nova chave será maior que a maior chave existente (isso evita duplicatas)
        if len(BOOKS) > 0:
            for book in BOOKS:
                x = int(book.split('_')[-1])
                if x > current_book_id:
                    current_book_id = x
                    
        new_key = f'book_{current_book_id + 1}' 
        
        BOOKS[new_key] = {
            'title': args['title'],
            'author': args['author']
        }
        
        # Requisição bem sucedida com criação de novo recurso no servidor
        return BOOKS[new_key], 201
        

class Book(Resource):
    @login_required
    def get(self, book_id):
        '''
            No Postman:
            GET
            localhost:5000/books/book_1 (ou qualquer chave do dicionário)
        '''
        
        self._abort_book_does_not_exist(book_id)
        return BOOKS[book_id]
    
    def delete(self, book_id):
        '''
            No Postman:
            DELETE
            localhost:5000/books/book_1 (ou qualquer chave do dicionário)
        '''
        
        self._abort_book_does_not_exist(book_id)
        
        del BOOKS[book_id]
        
        # Requisição retornada com sucesso, mas não há o que retornar.
        return '', 204
    
    def put(self, book_id):
        # extraindo os dados da requisição
        args = parser.parse_args()
        
        book_info = {'title': args['title'],
                     'author': args['author']}
        
        BOOKS[book_id] = book_info 
        
        # Requisição bem sucedida com criação de novo recurso no servidor
        return book_info, 201
    
    def _abort_book_does_not_exist(self, book_id):
        '''
            Método interno para tratar exceção do método 'get'.
        '''
        
        if book_id not in BOOKS:
            abort(404, message = f"Book {book_id} does not exist")

# adicionando os recursos criados à api
# <book_id> é um parâmetro de rota (parte dinâmica da URL)
api.add_resource(Book, "/books/<book_id>")
api.add_resource(BookList, "/books")

if __name__ == "__main__":
    
    # Inicia o servidor flask se o arquivo for executado.
    # 'debug = True' permite auto-reload e habilita o modo debug.
    app.run(debug = True)