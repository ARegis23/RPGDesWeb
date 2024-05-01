from flask import Flask, render_template, request, redirect, url_for, session
import repositorio

app = Flask (__name__)
app.secret_key = 'cQxuPDLQ3e5kcxRVrZNaC8Hvj9Lxyq34'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/listapersonagem.html")
def lista():
    lista_personagens = repositorio.retornar_personagens()
    return render_template("listapersonagem.html", dados = lista_personagens)

@app.route("/personagem/<int:id>", methods = ['GET', 'POST'])
def editar_personagem(id):

    if request.method == 'POST':
        if "excluir" in request.form:
            repositorio.remover_personagem(id)
            return redirect (url_for('lista'))
        #erro em salvar atualizações.
        elif "salvar" in request.form:
            id = request.form["id"]
            usuario = request.form["usuario"]
            personagem = request.form["personagem"]
            origem = request.form["origem"]
            level = request.form["level"]
            vida = request.form["vida"]
            dinheiro = request.form["dinheiro"]

            dados_retornados = repositorio.retornar_personagem(id)
            if dados_retornados:
                repositorio.atualizar_personagem(id = id, usuario = usuario, personagem = personagem, origem = origem, level = level, vida = vida, dinheiro = dinheiro)
            else:
                repositorio.criar_personagem(usuario= usuario, personagem= personagem, origem= origem, level= level, vida= vida, dinheiro= dinheiro)
            
            return redirect(url_for('lista'))
    else:
        #retorna os dados de um personagem na pagina de cadastro
        id, usuario, personagem, origem, level, vida, dinheiro = repositorio.retornar_personagem(id)
        
        return render_template("cadastro.html", id = id, usuario = usuario, personagem = personagem, origem = origem, level = level, vida = vida, dinheiro = dinheiro)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        # Verificar se o usuário já existe no banco de dados
        if not repositorio.verificar_usuario(email):
            # Se o usuário não existe, cadastrá-lo no banco de dados
            repositorio.cadastrar_usuario(email, senha)
            session['email'] = email  # Iniciar a sessão
            return redirect(url_for('lista'))
        
        # Se o usuário já existe, verificar a senha
        if repositorio.verificar_credenciais(email, senha):
            session['email'] = email  # Iniciar a sessão
            return redirect(url_for('lista'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos')
    else:
        return render_template('login.html')

@app.route("/esqueceu_senha")
def esqueceu_senha():
    # Lógica para lidar com o caso de esquecimento de senha
    return render_template('esqueceu_senha.html')


app.run(debug = True) 