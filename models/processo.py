from db import db

class ProcessoModel(db.Model):
    __tablename__ = 'Processos'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30))
    observacao = db.Column(db.String(300))

    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'))
    cliente = db.relationship('ClienteModel')

    def __init__(self, numero, observacao, cliente_id):
        self.numero = numero
        self.observacao = observacao
        self.cliente_id = cliente_id

    def json(self):
        return {'id': self.id, 
                'numero': self.numero, 
                'observacao': self.observacao, 
                'cliente_id': self.cliente_id
        }

    @classmethod
    def find_processos_cliente(cls, cliente_id):
        return cls.query.filter_by(cliente_id=cliente_id).all()

    @classmethod
    def find_processo_cliente_id(cls, cliente_id, processo_id):
        return cls.query.filter_by(cliente_id=cliente_id, id=processo_id).first()

    @classmethod
    def find_processos_cliente_numero(cls, cliente_id, numero):
        return cls.query.filter_by(cliente_id=cliente_id, numero=numero).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
