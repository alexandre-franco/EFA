from flask_restful import Resource, reqparse

from models.processo import ProcessoModel


from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)

class Processo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('numero',
                        required=True,
                        help="O numero do processo não pode ser vazio"
                        )
    parser.add_argument('observacao')

    @jwt_required
    def get(self, cliente_id, processo_id):
        processo = ProcessoModel.find_processo_cliente_id(cliente_id, processo_id)
        if processo:
            return processo.json()
        return {'mensagem': 'Processo do cliente não encontrado'}, 404

    @jwt_required
    def put(self, cliente_id, processo_id):
        
        data = Processo.parser.parse_args()

        processo = ProcessoModel.find_processo_cliente_id(cliente_id, processo_id)
        if not processo:
            processo = ProcessoModel.find_processos_cliente_numero(cliente_id, data['numero'])

        if processo:
            processo.numero = data['numero']
            processo.observacao = data['observacao']
        else: 
            processo = ProcessoModel(data['numero'], data['observacao'], cliente_id)

        try:
            processo.save_to_db()
        except:
            return {"mensagem": "Um erro ocorreu ao salvar o processo do cliente."}, 500

        return processo.json(), 201


    @jwt_required
    def delete(self, cliente_id, processo_id):
        claims = get_jwt_claims()
        if not claims['is admin']:
            return{'mensagem': 'Privilégios de adninistrador são necessários'}, 401

        processo = ProcessoModel.find_processo_cliente_id(cliente_id, processo_id)
        if processo:
            processo.delete_from_db()
            return {'mensagem': 'Processo do cliente removido.'}
        return {'mensagem': 'Processo do cliente não encontrado.'}, 404


class ProcessoLista(Resource):
    @jwt_required
    def get(self, cliente_id):
        return {'processos': [x.json() for x in ProcessoModel.find_processos_cliente(cliente_id)]}
