from db import db
from models.processo import ProcessoModel

class ClienteEnderecoModel(db.Model):
    __tablename__ = 'ClienteEnderecos'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))
    logradouro = db.Column(db.String(120))
    numero = db.Column(db.String(50))
    complemento = db.Column(db.String(50))
    cep = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))

    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'))
    cliente = db.relationship('ClienteModel')

    def __init__(self, tipo, logradouro, numero, complemento, cep, cidade, estado, cliente_id):
        self.tipo = tipo
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cep = cep
        self.cidade = cidade
        self.estado = estado
        self.cliente_id = cliente_id

    def json(self):
        return {'id': self.id, 
                'tipo': self.tipo, 
                'logradouro': self.logradouro, 
                'numero': self.numero,
                'complemento': self.complemento,
                'cep': self.cep,
                'cidade': self.cidade,
                'estado': self.estado,
                'cliente_id': self.cliente_id
        }

    @classmethod
    def busca_enderecos_cliente(cls, cliente_id):
        return cls.query.filter_by(cliente_id=cliente_id).all()

    @classmethod
    def busca_endereco_cliente_id(cls, cliente_id, endereco_id):
        return cls.query.filter_by(cliente_id=cliente_id, id=endereco_id).first()

    @classmethod
    def busca_endereco_cliente_tipo(cls, cliente_id, tipo):
        return cls.query.filter_by(cliente_id=cliente_id, tipo=tipo).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class ClienteEmailModel(db.Model):
    
    __tablename__ = 'ClienteEmails'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))
    email = db.Column(db.String(120))

    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'))
    cliente = db.relationship('ClienteModel')

    def __init__(self, tipo, email, cliente_id):
        self.tipo = tipo
        self.email = email
        self.cliente_id = cliente_id

    def json(self):
        return {'id': self.id, 
                'tipo': self.tipo, 
                'e-mail': self.email, 
                'cliente_id': self.cliente_id
        }

    @classmethod
    def busca_emails_cliente(cls, cliente_id):
        return cls.query.filter_by(cliente_id=cliente_id).all()
    
    @classmethod
    def busca_email_cliente_id(cls, cliente_id, endereco_id):
        return cls.query.filter_by(cliente_id=cliente_id, id=endereco_id).first()

    @classmethod
    def busca_email_cliente_tipo(cls, cliente_id, tipo):
        return cls.query.filter_by(cliente_id=cliente_id, tipo=tipo).first()    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class ClienteTelefoneModel(db.Model):
    
    __tablename__ = 'ClienteTelefones'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))
    telefone = db.Column(db.String(30))

    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'))
    cliente = db.relationship('ClienteModel')

    def __init__(self, tipo, telefone, cliente_id):
        self.tipo = tipo
        self.telefone = telefone
        self.cliente_id = cliente_id

    def json(self):
        return {'id': self.id, 
                'tipo': self.tipo, 
                'telefone': self.telefone, 
                'cliente_id': self.cliente_id
        }

    @classmethod
    def busca_telefones_cliente(cls, cliente_id):
        return cls.query.filter_by(cliente_id=cliente_id).all()
    
    @classmethod
    def busca_telefone_cliente_id(cls, cliente_id, telefone_id):
        return cls.query.filter_by(cliente_id=cliente_id, id=telefone_id).first()

    @classmethod
    def busca_telefone_cliente_tipo(cls, cliente_id, tipo):
        return cls.query.filter_by(cliente_id=cliente_id, tipo=tipo).first()    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class ClienteModel(db.Model):
    __tablename__ = 'Clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    cnpj = db.Column(db.String(20))
    cpf = db.Column(db.String(20))

    enderecos = db.relationship('ClienteEnderecoModel', lazy='dynamic')
    emails = db.relationship('ClienteEmailModel', lazy='dynamic')
    telefones = db.relationship('ClienteTelefoneModel', lazy='dynamic')
    processos = db.relationship('ProcessoModel', lazy='dynamic')

    observacao = db.Column(db.String(2000))

    def __init__(self, nome, cnpj, cpf, observacao):
        self.nome = nome
        self.cnpj = cnpj
        self.cpf = cpf
        self.observacao = observacao

    def json(self):
        return {'id': self.id, 
                'nome': self.nome, 
                'cnpj': self.cnpj, 
                'cpf': self.cpf,
                'enderecos': [endereco.json() for endereco in self.enderecos.all()],
                'e-mails': [email.json() for email in self.emails.all()],
                'telefones': [telefone.json() for telefone in self.telefones.all()],
                'observacao': self.observacao
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def find_by_cnpj(cls, cpf):
        return cls.query.filter_by(cpf=cpf).first()

    @classmethod
    def find_by_cpf(cls, cpf):
        return cls.query.filter_by(cpf=cpf).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
