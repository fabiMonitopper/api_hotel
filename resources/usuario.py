
from operator import attrgetter
from flask_restful import Resource, reqparse
from sqlalchemy import Identity
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="campo 'login' não pode ser deixado em branco ")
atributos.add_argument('senha', type=str, required=True, help="campo 'Senha' não pode ser deixado em branco ")

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404  

    @jwt_required   
    def delete(self, user_id): 
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return{'message':'Erro ao deletar o Hotel '}, 500
            return {'message': 'User deleted'}
        return {'messege': 'User not found.'}, 404

class UserRegister(Resource):
    def post(self):
        
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return{"message": "The login '{}' already exists.".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User cread successfully!'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {' message': 'Logged out successfully!'}



# Houve uma atualização da biblioteca flask_jwt_extended, e uma série de coisas foram renomeadas. Para acompanhar a 
# aula com a biblioteca atualizada você precisará fazer as seguintes adaptações:
# - Substitua @jwt_required por ===> @jwt_required()
# - Renomeie @jwt.token_in_blacklist_loader para ===>  @jwt.token_in_blocklist_loader
# - Substitua get_raw_jwt por ===> get_jwt

# - Na função def verifica_blacklist(token): acrescente um self na frente do token: ===> def verifica_blacklist(self,token):
# Pode ser que funcione com apenas essas adaptações. Teste, e se ainda assim obtiver algum erro, adicione duas variáveis 
# (jwt_header, jwt_payload) na função token_de_acesso_invalidado:
# Antes def token_de_acesso_invalidado():   ===> Depois def token_de_acesso_invalidado(jwt_header, jwt_payload):
# Com essas alterações, você conseguirá acompanhar o curso.