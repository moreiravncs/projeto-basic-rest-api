from flask_restful import Api, Resource, abort, reqparse
from flask import Flask, request, make_response
from functools import wraps
from config import USERNAME, PASSWORD
from books_data import BOOKS


# Entrypoint para a aplicação Flask
app = Flask(__name__)

# Entrypoint da aplicação para o Flask RESTful
api = Api(app)


# 'event' é a função que será decorada
# 'login_required' será o nome do decorador
def login_required(event):
    
    # O decorador 'wraps' preserva a função a ser decorada (sem ele o nome dela passaria a ser 'login')
    @wraps(event)
    def login(*args, **kwargs):
        '''
            Essa função intercepta a chamada original, checa as credenciais
            e decide se a função será executada ou não.
            *args e **kwargs é porque a assinatura da função decorada é desconhecida.
        '''
        
        # Verifica se possui cabeçalho de autenticação e se as credenciais estão corretas
        if request.authorization and  \
        request.authorization.username == USERNAME and \
        request.authorization.password == PASSWORD:
            return event(*args, **kwargs)
        
        # {'WWW-Authenticate': 'Basic realm="Login Realm"'} é especificação oficial para autenticação básica do HTTP
        return make_response('Could not verify your credentials',
                             401,
                             {'WWW-Authenticate': 'Basic realm="Login Realm"'})
    
    return login


# RequestParser cria um "validador" de argumentos da requisição
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('author')


"""
    'Resource' é uma classe abstrata, a implementação concreta dela
    deve herdar da mesma e expor os métodos http.
    
    Não é possível que uma mesma classe do tipo 'Resource' possua dois 
    métodos 'get', por exemplo. E isso se aplica aos demais métodos http.
"""
        

class Book(Resource):
    @login_required
    def get(self, book_id):
        '''
            Retorna um registro específico.
            
            Para testar no Postman:
            GET
            localhost:5000/books/book_1 (ou qualquer chave do dicionário)
        '''
        
        self._abort_book_does_not_exist(book_id)
        
        return BOOKS[book_id]
    
    def delete(self, book_id):
        '''
            Exclui um registro específico.
            
            No Postman:
            DELETE
            localhost:5000/books/book_1 (ou qualquer chave do dicionário)
        '''
        
        self._abort_book_does_not_exist(book_id)
        
        del BOOKS[book_id]
        
        # Requisição retornada com sucesso, mas não há dados para retornar
        return '', 204
    
    def put(self, book_id):
        '''
            Atualiza um registro.
        '''
        
        # extraindo os dados da requisição
        args = parser.parse_args()
        
        book_info = {'title': args['title'],
                     'author': args['author']}
        
        BOOKS[book_id] = book_info 
        
        # Requisição bem sucedida com a atualização do recurso no servidor
        return book_info, 201
    
    def _abort_book_does_not_exist(self, book_id):
        '''
            Método interno para tratar exceção de 'book_id' inválido.
        '''
        
        if book_id not in BOOKS:
            abort(404, message = f"Book {book_id} does not exist")


class BookList(Resource):
    def get(self):
        '''
            Retorna todos os dados.
        '''
        
        return BOOKS
    
    def post(self):
        '''
            Cria um novo registro no "banco de dados".
        '''
        
        args = parser.parse_args()
        
        current_book_id = 0
        
        # Garantindo que o nova chave será maior que a maior chave existente
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


# Adicionando os recursos criados à api
# '<book_id>' é um parâmetro de rota (parte dinâmica da URL)
api.add_resource(Book, "/books/<book_id>")
api.add_resource(BookList, "/books")


if __name__ == "__main__":
    
    # Inicia o servidor flask se esse arquivo for executado
    # 'debug = True' permite auto-reload e habilita o modo debug
    app.run(debug = True)