from flask_restful import Resource, reqparse

from models.cliente import (
    ClienteModel, 
    ClienteEmailModel, 
    ClienteEnderecoModel, 
    ClienteTelefoneModel
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)

class Cliente(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nome',
                        required=True,
                        help="O nome não pode ser vazio"
                        )
    parser.add_argument('cnpj')
    parser.add_argument('cpf')
    parser.add_argument('observacao')

    @jwt_required
    def get(self, cliente_id):
        cliente = ClienteModel.find_by_id(cliente_id)
        if cliente:
            return cliente.json()
        return {'mensagem': 'Cliente não encontrado'}, 404

    @jwt_required
    def put(self, cliente_id):
        
        data = Cliente.parser.parse_args()

        cliente = ClienteModel.find_by_nome(data['nome'])
        if not cliente:
            cliente = ClienteModel.find_by_cnpj(data['cnpj'])
        if not cliente:
            cliente = ClienteModel.find_by_cpf(data['cpf'])

        if cliente:
            cliente.nome = data['nome']
            cliente.cnpj = data['cnpj']
            cliente.cpf = data['cpf']
            cliente.observacao = data['observacao']
        else: 
            cliente = ClienteModel(**data)

        try:
            cliente.save_to_db()
        except:
            return {"mensagem": "Um erro ocorreu ao salvar o cliente."}, 500

        return cliente.json(), 201


    @jwt_required
    def delete(self, cliente_id):
        claims = get_jwt_claims()
        if not claims['is admin']:
            return{'mensagem': 'Privilégios de adninistrador são necessários'}, 401

        cliente = ClienteModel.find_by_id(cliente_id)
        if cliente:
            cliente.delete_from_db()
            return {'mensagem': 'Cliente removido.'}
        return {'mensagem': 'Cliente não encontrado.'}, 404


class ClienteEndereco(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tipo',
                        required=True,
                        help="O tipo não pode ser vazio"
                        )
    parser.add_argument('logradouro',
                        required=True,
                        help="O lograqdouro não pode ser vazio"
                        )
    parser.add_argument('numero',
                        required=True,
                        help="O numero não pode ser vazio"
                        )
    parser.add_argument('complemento')
    parser.add_argument('cep',
                        required=True,
                        help="O cep não pode ser vazio"
                        )
    parser.add_argument('cidade',
                        required=True,
                        help="A cidade não pode ser vazia"
                        )
    parser.add_argument('estado',
                        required=True,
                        help="O estado não pode ser vazio"
                        )

    @jwt_required
    def get(self, cliente_id, endereco_id):
        endereco = ClienteEnderecoModel.busca_endereco_cliente_id(cliente_id, endereco_id)

        if endereco:
            return endereco.json()
        return {'mensagem': 'Endereço do cliente não encontrado'}, 404

    @jwt_required
    def put(self, cliente_id, endereco_id):
        
        data = ClienteEndereco.parser.parse_args()

        endereco = ClienteEnderecoModel.busca_endereco_cliente_id(cliente_id, endereco_id)

        if not endereco:
            endereco = ClienteEnderecoModel.busca_endereco_cliente_tipo(cliente_id, data['tipo'])

        if endereco:
            endereco.tipo = data['tipo']
            endereco.logradouro = data['logradouro']
            endereco.numero = data['numero']
            endereco.complemento = data['complemento']
            endereco.cep = data['cep']
            endereco.cidade = data['cidade']
            endereco.estado = data['estado']
        else: 
            endereco = ClienteEnderecoModel(data['tipo'], data['logradouro'], data['numero'], data['complemento'],data['cep'],
                                            data['cidade'], data['estado'], cliente_id)

        try:
            endereco.save_to_db()
        except:
            return {"mensagem": "Um erro ocorreu ao salvar o endereço do cliente."}, 500

        return endereco.json(), 201


    @jwt_required
    def delete(self, cliente_id, endereco_id):
        claims = get_jwt_claims()
        if not claims['is admin']:
            return{'mensagem': 'Privilégios de adninistrador são necessários'}, 401

        endereco = ClienteEnderecoModel.busca_endereco_cliente_id(cliente_id, endereco_id)
        if endereco:
            endereco.delete_from_db()
            return {'mensagem': 'Endereço do cliente removido.'}
        return {'mensagem': 'Endereço do cliente não encontrado.'}, 404

class ClienteTelefone(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tipo',
                        required=True,
                        help="O tipo não pode ser vazio"
                        )
    parser.add_argument('telefone',
                        required=True,
                        help="O telefone não pode ser vazio"
                        )

    @jwt_required
    def get(self, cliente_id, telefone_id):
        telefone = ClienteTelefoneModel.busca_telefone_cliente_id(cliente_id, telefone_id)

        if telefone:
            return telefone.json()
        return {'mensagem': 'Telefone do cliente não encontrado'}, 404

    @jwt_required
    def put(self, cliente_id, telefone_id):
        
        data = ClienteTelefone.parser.parse_args()

        telefone = ClienteTelefoneModel.busca_telefone_cliente_id(cliente_id, telefone_id)

        if not telefone:
            telefone = ClienteTelefoneModel.busca_telefone_cliente_tipo(cliente_id, data['tipo'])

        if telefone:
            telefone.tipo = data['tipo']
            telefone.telefone = data['telefone']
        else: 
            telefone = ClienteTelefoneModel(data['tipo'], data['telefone'], cliente_id)

        try:
            telefone.save_to_db()
        except:
            return {"mensagem": "Um erro ocorreu ao salvar o telefone do cliente."}, 500

        return telefone.json(), 201


    @jwt_required
    def delete(self, cliente_id, telefone_id):
        claims = get_jwt_claims()
        if not claims['is admin']:
            return{'mensagem': 'Privilégios de adninistrador são necessários'}, 401

        telefone = ClienteTelefoneModel.busca_telefone_cliente_id(cliente_id, telefone_id)
        if telefone:
            telefone.delete_from_db()
            return {'mensagem': 'Telefone do cliente removido.'}
        return {'mensagem': 'Telefone do cliente não encontrado.'}, 404

class ClienteEmail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tipo',
                        required=True,
                        help="O tipo não pode ser vazio"
                        )
    parser.add_argument('email',
                        required=True,
                        help="O e-mail não pode ser vazio"
                        )

    @jwt_required
    def get(self, cliente_id, email_id):
        email = ClienteEmailModel.busca_email_cliente_id(cliente_id, email_id)

        if email:
            return email.json()
        return {'mensagem': 'E-mail do cliente não encontrado'}, 404

    @jwt_required
    def put(self, cliente_id, email_id):
        
        data = ClienteEmail.parser.parse_args()

        email = ClienteEmailModel.busca_email_cliente_id(cliente_id, email_id)

        if not email:
            email = ClienteEmailModel.busca_email_cliente_tipo(cliente_id, data['tipo'])

        if email:
            email.tipo = data['tipo']
            email.email = data['email']
        else: 
            email = ClienteEmailModel(data['tipo'], data['email'], cliente_id)

        try:
            email.save_to_db()
        except:
            return {"mensagem": "Um erro ocorreu ao salvar o e-mail do cliente."}, 500

        return email.json(), 201


    @jwt_required
    def delete(self, cliente_id, email_id):
        claims = get_jwt_claims()
        if not claims['is admin']:
            return{'mensagem': 'Privilégios de adninistrador são necessários'}, 401

        email = ClienteEmailModel.busca_email_cliente_id(cliente_id, email_id)
        if email:
            email.delete_from_db()
            return {'mensagem': 'E-mail do cliente removido.'}
        return {'mensagem': 'E-Mail do cliente não encontrado.'}, 404


class ClienteLista(Resource):
    @jwt_required
    def get(self):
        return {'clientes': [x.json() for x in ClienteModel.find_all()]}


class ClienteEnderecoLista(Resource):
    @jwt_required
    def get(self, cliente_id):
        return {'enderecos': [x.json() for x in ClienteEnderecoModel.busca_enderecos_cliente(cliente_id)]}


class ClienteTelefoneLista(Resource):
    @jwt_required
    def get(self, cliente_id):
        return {'telefones': [x.json() for x in ClienteTelefoneModel.busca_telefones_cliente(cliente_id)]}


class ClienteEmailLista(Resource):
    @jwt_required
    def get(self, cliente_id):
        return {'emails': [x.json() for x in ClienteEmailModel.busca_emails_cliente(cliente_id)]}
