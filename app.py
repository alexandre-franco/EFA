from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh

from resources.cliente import (
    Cliente,
    ClienteLista, 
    ClienteEndereco, 
    ClienteEnderecoLista,
    ClienteTelefone, 
    ClienteTelefoneLista,
    ClienteEmail, 
    ClienteEmailLista,
)

from resources.processo import Processo, ProcessoLista
from resources.honorario import Honorario, HonorarioLista
from resources.custa import Custa, CustaLista


from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'jose'
api = Api(app)

    
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is admin': True}
    return {'is admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorizaiton_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(ClienteLista, '/clientes')
api.add_resource(Cliente, '/cliente/<int:cliente_id>')
api.add_resource(ClienteEndereco, '/cliente/<int:cliente_id>/enderecos/<int:endereco_id>')
api.add_resource(ClienteEnderecoLista, '/cliente/<int:cliente_id>/enderecos/')
api.add_resource(ClienteTelefone, '/cliente/<int:cliente_id>/telefones/<int:telefone_id>')
api.add_resource(ClienteTelefoneLista, '/cliente/<int:cliente_id>/telefones/')
api.add_resource(ClienteEmail, '/cliente/<int:cliente_id>/emails/<int:email_id>')
api.add_resource(ClienteEmailLista, '/cliente/<int:cliente_id>/emails/')

api.add_resource(Processo, '/cliente/<int:cliente_id>/processos/<int:processo_id>')
api.add_resource(ProcessoLista, '/cliente/<int:cliente_id>/processos/')

api.add_resource(HonorarioProcesso, '/cliente/<int:cliente_id>/processos/<int:processo_id>/honorarios<int:honorario_id>')
api.add_resource(HonorarioProcessoLista, '/cliente/<int:cliente_id>/processos/honorarios/')

api.add_resource(CustaProcesso, '/cliente/<int:cliente_id>/processos/<int:processo_id>/custas<int:custa_id>')
api.add_resource(CustaProcessoLista, '/cliente/<int:cliente_id>/processos/custas/')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
