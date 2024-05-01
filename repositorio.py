import sqlite3

#funcao que gera um novo id
def gerar_id():
    conn = sqlite3.connect("RPG.db")
    cursor = conn.cursor()
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = 'personagens'")
    next_id = cursor.fetchone()[0]
    return next_id + 1

#funcao que CRIA novo personagem
def criar_personagem(usuario, personagem, origem, level, vida, dinheiro):
    try:
        conn = sqlite3.connect("RPG.db")
        cursor = conn.cursor()
        sql_insert = " INSERT INTO personagens (usuario_personagem, personagem_personagem, origem_personagem, level_personagem, vida_personagem, dinheiro_personagem) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(sql_insert, (usuario, personagem, origem, level, vida, dinheiro))
        personagem_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return personagem_id
    except Exception as ex:
        print(ex)
        return 0

#funcao RETORNA todos os personagens
def retornar_personagens():
    try:
        conn = sqlite3.connect("RPG.db")
        cursor = conn.cursor()
        sql_select = "SELECT * FROM personagens"
        cursor.execute(sql_select)
        personagens = cursor.fetchall()
        conn.close()
        return personagens
    except:
        return False

#funcao RETORNA um unico personagem 
def retornar_personagem(id:int):
    try:
        if id == 0:
            return gerar_id(), "", "", "", "", "",""
        conn = sqlite3.connect("RPG.db")
        cursor = conn.cursor()

        sql_select = "SELECT * FROM personagens WHERE id_personagem = ?"
        cursor.execute(sql_select, (id, ))
        id, usuario, personagem, origem, level, vida, dinheiro = cursor.fetchone()
        conn.close()
        return id, usuario, personagem, origem, level, vida, dinheiro
    except:
        return False

#funcao ATUALIZA os dados de um personagem
def atualizar_personagem(id:int, usuario, personagem, origem, level, vida, dinheiro):
    try:
        #tentar atualizar
        conn = sqlite3.connect("RPG.db")
        cursor = conn.cursor()
        sql_update = "UPDATE personagens SET usuario_personagem = ?, personagem_personagem = ?, origem_personagem = ?, level_personagem = ?, vida_personagem = ?, dinheiro_personagem = ? WHERE id_personagem = ?"
        cursor.execute(sql_update, (usuario, personagem, origem, level, vida, dinheiro, id))
        conn.commit()
        conn.close()
        return True

    except Exception as ex:
        print(ex)
        return False

#funcao REMOVE um personagem
def remover_personagem(id:int):
    try:
        conn = sqlite3.connect("RPG.db")
        cursor = conn.cursor()
        sql_delete = "DELETE FROM personagens WHERE id_personagem = ?"
        cursor.execute(sql_delete, (id, ))
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        return False

#funcao para verificar usuario
def verificar_usuario(email):
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

def cadastrar_usuario(email, senha):
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
    conn.commit()
    conn.close()

def verificar_credenciais(email, senha):
    try:
        conn = sqlite3.connect("login.db")
        cursor = conn.cursor()
        sql_select = "SELECT * FROM usuarios WHERE email = ? AND senha = ?"
        cursor.execute(sql_select, (email, senha))
        usuario_encontrado = cursor.fetchone()
        conn.close()
        if usuario_encontrado:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Erro ao verificar credenciais:", e)
        return False

'''
#testes:

usuario = "Alisson"
personagem = "Sven"
origem = "Imperial"
level = "7"
vida = "10"
dinheiro = "100"

id = criar_personagem(usuario, personagem, origem, level, vida, dinheiro)
print(id)
print(retornar_personagem(id))

id, usuario, personagem, origem, level, vida, dinheiro = retornar_personagem(id)
atualizar_personagem(id, "Alisson Regis", personagem, origem, level, vida, dinheiro)

print(retornar_personagem(id))
id, usuario, personagem, origem, level, vida, dinheiro = retornar_personagem(id)

print(retornar_personagens())

#remover_personagem(id)

print(retornar_personagens())
'''