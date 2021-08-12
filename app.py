from flask import Flask, render_template, request, redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
import classes

global output
output = list()

app = classes.app #puxar app da classes
db = classes.db #puxar o bd da classes

#-----métodos para mudança de exibição dos botões de acordo com login do usuário--------------------------------------
@app.context_processor
def valor_log():
    if 'id_logado' not in session or session['id_logado'] == None:
        return dict(log=False)
    else:
        return dict(log=True)      
#----------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/favicon.ico")
def principal():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    prox=request.args.get('prox')
    return render_template('login.html',prox=prox)

#----------acrescimo nikolas-----------------------------------
@app.route('/logout')
def logout():
    session['id_logado'] = None
    return redirect('/')

@app.route('/deletar_cadastro', methods=['GET','POST'])
def deletar_cadastro():
    sucesso=False
    id = session['id_logado']
    cliente = classes.Clientes.query.get(id)
    id_pagamento = classes.Forma_pagamento.consultar_id_pagamento(id)
    info_pagamento = classes.Forma_pagamento.query.get(id_pagamento)
    info_pagamento.delete()
    id_endereco = classes.Enderecos.consultar_id_endereco(id)
    info_endereco = classes.Enderecos.query.get(id_endereco)
    info_endereco.delete()
    cliente = classes.Clientes.query.get(id)
    datos=cliente
    cliente.delete()
    sucesso=True
    return render_template('index.html', datos=datos, sucesso=sucesso)


@app.route('/editar_cadastro', methods=['GET','POST'])
def editar_cadastro():
    if request.method == 'GET':
        id = session['id_logado']
        editar_cliente = classes.Clientes.query.get(id)
        editar_endereco = classes.Enderecos.query.get(id)
        editar_pagamento = classes.Forma_pagamento.query.get(id)
        return render_template('editar.html',editar_cliente=editar_cliente,
                                            editar_endereco=editar_endereco,
                                            editar_pagamento=editar_pagamento)

    elif request.method == 'POST':
        id = session['id_logado']
        editar_cliente = classes.Clientes.query.get(id)
        editar_cliente.nome = request.form['novo_nome']
        editar_cliente.sobrenome = request.form['novo_sobrenome']
        editar_cliente.telefone = request.form['novo_telefone']
        editar_cliente.email = request.form['novo_email']
        editar_cliente.usuario = request.form['novo_usuario']
        editar_cliente.senha1 = request.form['novo_senha1']
        editar_cliente.senha = request.form['novo_senha']

        editar_endereco = classes.Enderecos.query.get(id)
        editar_endereco.cep = request.form['novo_cep']
        editar_endereco.rua = request.form['novo_rua']
        editar_endereco.numero = request.form['novo_numero']
        editar_endereco.complemento = request.form['novo_complemento']

        editar_pagamento = classes.Forma_pagamento.query.get(id)
        editar_pagamento.numero_cartao = request.form['novo_numero_cartao']
        editar_pagamento.nome_cartao = request.form['novo_nome_cartao']
        editar_pagamento.cpf = request.form['novo_cpf']
        editar_pagamento.mes_vencimento = request.form['novo_mes_vencimento']
        editar_pagamento.ano_vencimento = request.form['novo_ano_vencimento']

        db.session.commit()
        return redirect(url_for('index'))

#--------------------------------------------------------------

@app.route('/menu', methods=['GET','POST'])
def menu():
    if 'id_logado' not in session or session['id_logado'] == None:
        return redirect(url_for('login',prox=url_for('menu')))
    elif 'id_logado' in session:
        produtos = classes.Produtos.produtos_read_all()
        return render_template('menu.html', produtos=produtos)
    
        


@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    #caso tenha cadastro no BD
    novo_cadastro = None
    existe = None
    cnome = None
    csobrenome = None
    if (request.method == 'POST'):
        form = request.form
        email = form['email']
        existe_email= classes.Clientes.consultar_email(email)

        #Verifica a existencia do e-mail no BD   
        if existe_email == True:
            existe = "Seu email encontra-se cadastrado em nosso sistema"
            novo_cadastro = True

        #----------acrescimo nikolas--------------------------------------------------------------------------------
            info_cliente = classes.Clientes.query.filter_by(email=email).first()
            if request.form['senha']==info_cliente.senha:
                session['id_logado'] = info_cliente.id_cliente        
                prox_pag = request.form['prox']
                return redirect(prox_pag)
            """return render_template('cadastro.html', existe=existe, novo_cadastro = novo_cadastro, email=email)"""
        #-----------------------------------------------------------------------------------------------------------

        #caso não tenha cadastro no BD   
        novo_cliente = classes.Clientes(nome=form['nome'], sobrenome=form['sobrenome'], email=form['email'], telefone=form['telefone'], usuario=form['usuario'], senha=form['senha'])
        db.session.add(novo_cliente)
        db.session.commit()
        
        #caso ocorra erro no cadastro  
        id_cliente = classes.Clientes.consultar_id(email)
        if id_cliente == None:
            existe = "Ocorreu um erro, por favor tente cadastrar novamento"
            novo_cadastro = True
            return render_template('cadastro.html', existe=existe, novo_cadastro = novo_cadastro)

        #caso o cadastro dê certo
        novo_endereco = classes.Enderecos(id_cliente=id_cliente, cep=form['cep'], numero=form['numero'], rua=form['rua'], complemento=form['complemento'])
        db.session.add(novo_endereco)
        db.session.commit()

        novo_forma_pagamento = classes.Forma_pagamento(id_cliente=id_cliente, numero_cartao=form['numero_cartao'], cpf=form['cpf'], nome=form['nome_cartao'], validade_mes=form['mes_vencimento'], validade_ano=form['ano_vencimento'])
        db.session.add(novo_forma_pagamento)
        db.session.commit()

        novo_cadastro = True
        cnome= form['nome']
        csobrenome = form['sobrenome']
    return render_template('cadastro.html', novo_cadastro=novo_cadastro, cnome=cnome, csobrenome=csobrenome)


@app.route('/finalizar_pedido')
def carrinho2():
    registros = list()
    total = 0
    for id in output:
        r = dict()
        datos = classes.Produtos.produtos_read_id(id)
        r["nome"] = datos.nome
        r["link_img"] = datos.link_img
        r["preco"] = datos.preco
        r["descricao"] = datos.descricao
        total = datos.preco + total
        registros.append(r)
    return render_template('detalhes.html', output=registros, total=total)

@app.route('/clear')
def clear(): 
   output.clear() 
   return redirect('/menu')


class carrinho():
    def __init__(self, id_produto):
        self.id_produto = id_produto

    @staticmethod
    def contar_p(id_produto):
        output.append(id_produto)
        return output


@app.route('/<id_produto>', methods=['GET','POST'])
def ver_produto(id_produto):
    detalhes = carrinho.contar_p(id_produto)
    return redirect('/menu')


@app.route('/sobre')
def sobre():
    return render_template('faleconosco.html')

if (__name__ == '__main__'):
    db.create_all()
    app.run(debug=True)
    exit()
