from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configuracoes de acceso ao banco de dados
user='xqtbbsoy'
password='BIjm6OQGv7Q-F0JC5LouLKvC8TtDhMsT'
host='kesavan.db.elephantsql.com'
database='xqtbbsoy'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key ="pepe pepe pepe"

#Intanciando objeto da Classe SQLAlchemy 
db = SQLAlchemy(app)


#___Classes______________________________________________________________________

class Clientes(db.Model):
    __tablename__= "clientes"
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    sobrenome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(255), nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def __init__(self, nome, sobrenome, email, telefone, usuario, senha):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.telefone = telefone
        self.usuario = usuario
        self.senha = senha

    @staticmethod
    def clientes_read_all():
         # SELECT * from produtos ORDER BY id ASC
         return Clientes.query.order_by(Clientes.id_cliente.asc()).all()


    @staticmethod
    def consultar_email(email):
         all_clientes = Clientes.query.order_by(Clientes.id_cliente.asc()).all()
         for cliente in all_clientes:  
            if (cliente.email == email):
                return True      
         return False   

    @staticmethod
    def consultar_id(email):
         all_clientes = Clientes.query.order_by(Clientes.id_cliente.asc()).all()
         for cliente in all_clientes:  
            if (cliente.email == email):
                return cliente.id_cliente
         return None 

    def delete(self):
        db.session.delete(self)
        db.session.commit() 

class Enderecos(db.Model):
    __tablename__= "enderecos"
    id_endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, nullable=False)
    cep = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    complemento = db.Column(db.String(255), nullable=True)

    def __init__(self, id_cliente, cep, numero, rua, complemento):
        self.id_cliente = id_cliente
        self.cep = cep
        self.numero = numero
        self.rua = rua
        self.complemento = complemento

    @staticmethod
    def consultar_id_endereco(id_cliente):
         all_enderecos = Enderecos.query.order_by(Enderecos.id_endereco.asc()).all()
         for cliente in all_enderecos: 
            if (cliente.id_cliente == id_cliente):
                return cliente.id_endereco    
         return False

    def delete(self):
        db.session.delete(self)
        db.session.commit() 
    
class Forma_pagamento(db.Model):
    __tablename__= "forma_pagamento"
    id_pagamento = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_cliente = db.Column(db.Integer, nullable=False)
    numero_cartao = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    validade_mes = db.Column(db.Integer, nullable=False)
    validade_ano = db.Column(db.Integer, nullable=False)

    def __init__(self, id_cliente, numero_cartao, cpf, nome, validade_mes, validade_ano):
        self.id_cliente = id_cliente
        self.numero_cartao = numero_cartao
        self.cpf = cpf
        self.nome = nome
        self.validade_mes = validade_mes
        self.validade_ano = validade_ano

    @staticmethod
    def consultar_id_pagamento(id_cliente):
         all_pagamentos = Forma_pagamento.query.order_by(Forma_pagamento.id_pagamento.asc()).all()
         for cliente in all_pagamentos:  
            if (cliente.id_cliente == id_cliente):
                return cliente.id_pagamento     
         return False 


    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Produtos(db.Model):
    __tablename__= "produtos"
    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    link_img = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    
    def __init__(self, nome, descricao, link_img, preco, categoria, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.link_img = link_img
        self.preco = preco
        self.categoria = categoria
        self.quantidade = quantidade

    @staticmethod
    def produtos_read_all():
         # SELECT * from produtos ORDER BY id ASC
         return Produtos.query.order_by(Produtos.id_produto.asc()).all()

    @staticmethod
    def produtos_read_id(id):
         return Produtos.query.get(id)

class Pedidos(db.Model):
    __tablename__= "pedidos"
    id_pedidos = db.Column(db.Integer, primary_key=True,autoincrement=True)
    id_cliente = db.Column(db.Integer, nullable=False)
    id_endereco = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, nullable=False)
    observacao = db.Column(db.String(255), nullable=True)
    valor_total = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Boolean)
    
    def __init__(self, id_cliente, id_endereco, data, observacao, valor_total, estado):
        self.id_cliente =id_cliente
        self.id_endereco = id_endereco
        self.data = data
        self.observacao = observacao
        self.valor_total = valor_total
        self.estado = estado


class Pedido_produto(db.Model):
    __tablename__= "pedido_produto"
    id_p = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, nullable=False)
    id_produto = db.Column(db.Integer, nullable=False)

    def __init__(self, id_pedido, id_produto):
        self.id_pedido = id_pedido
        self.id_produto = id_produto

