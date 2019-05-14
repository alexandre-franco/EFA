from flask_restful import Resource, reqparse

from models.honorario import CustaModel


from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity,
    fresh_jwt_required
)

class HonorarioCusta:
    parser = reqparse.RequestParser()
    parser.add_argument('forma_pagamento',
                        required=True,
                        help="a forma de pagamento não pode ser vazia"
                        )
    parser.add_argument('valor',
                        type=float,
                        required=True,
                        help="o valor não pode ser vazio"
                        )
    parser.add_argument('data_vencimento',
                        required=True,
                        help="A data de vencimento não pode ser vazia"
                        )
    parser.add_argument('situacao',
                        required=True,
                        help="A situacao não pode ser vazia"
                        )
    parser.add_argument('historico')

    @jwt_required
    def get(self, cliente_id, processo_id, honorario_id):
        honorario = HonorarioModel.find_honodario_processo_cliente_id(cliente_id, processo_id, honorario_id)
        if honorario:
            return honorario.json()
        return {'mensagem': 'Honorário do processo do cliente não encontrado'}, 404

    @jwt_required
    def put(self, cliente_id, processo_id, honorario_id):
        
        data = Honorario.parser.parse_args()

        honorario = ProcessoModel.find_honorario_processo_cliente_id(cliente_id, processo_id, honorario_id)

        if honorario:
            honorario.forma_pagamento = data['forma_pagamento']
            honorario.valor = data['valor']
            honorario.data_vencimento = data['data_vencimento']
            honorario.situacao = data['situacao']
            honorario.historico = data['historico']
        else: 
            honorario = HonorarioModel(cliente_id, processo_id, **data)

        try:
            honorario.save_to_db()
        except:
            return {"mensagem": "Um erro ocorreu ao salvar o honorário do processo do cliente."}, 500

        return honorario.json(), 201


    @jwt_required
    def delete(self, cliente_id, processo_id, honorario_id):
        claims = get_jwt_claims()
        if not claims['is admin']:
            return{'mensagem': 'Privilégios de adninistrador são necessários'}, 401

        honorario = HonorarioModel.find_honorario_processo_cliente_id(cliente_id, processo_id, honorario_id)
        if honorario:
            honorario.delete_from_db()
            return {'mensagem': 'Honorario do processo do cliente removido.'}
        return {'mensagem': 'Honorario do processo do cliente não encontrado.'}, 404


class HonorarioLista(Resource):
    @jwt_required
    def get(self, cliente_id, processo_id):
        return {'honorarios': [x.json() for x in HonorariosModel.find_honorarios_processos_cliente(cliente_id, processo_id)]}
