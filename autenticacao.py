import sqlite3

def conectarBD():
    conn = sqlite3.connect('gerenciadorSenhas.db')
    conn.execute("PRAGMA foreign_keys = ON;") #Ativa o uso de foreign key
    return conn


def entrar():
    conn = conectarBD()
    cursor = conn.cursor()

    usuario = input("\nUsuário: ")
    senha = input("Senha Mestra: ")

    cursor.execute("SELECT id FROM usuario WHERE nome = ? AND senhaMestra = ?", (usuario, senha))
    resultado = cursor.fetchone()

    if resultado:
        print("Login bem-sucedido!")
        return resultado[0]

    else:
        print("Usuário ou senha incorretos.")
        return None


def cadastrar():
    conn = conectarBD()
    cursor = conn.cursor()

    nome = input("\nNome de usuário: ")
    cursor.execute("SELECT id FROM usuario WHERE nome = ?", (nome,))
    if cursor.fetchone():
        print("Nome de usuário já cadastrado\n")
        return None

    senha = input("Crie sua senha mestra: ")
    senha2 = input("Confirme sua senha: ")

    if senha != senha2:
        print("As senhas não coincidem.")
        return None

    cursor.execute("INSERT INTO usuario (nome, senhaMestra) VALUES (?, ?)", (nome, senha))
    conn.commit()
    print("Usuário cadastrado com sucesso!")
    return cursor.lastrowid




# def exibir():
#     conn = conectarBD()
#     cursor = conn.cursor()

#     print("\n=== USUÁRIOS CADASTRADOS ===")
#     cursor.execute("SELECT id, nome FROM usuario")
#     usuarios = cursor.fetchall()

#     if usuarios:
#         for usuario in usuarios:
#             print(f"ID: {usuario[0]} | Nome: {usuario[1]}")
#     else:
#         print("Nenhum usuário cadastrado ainda.")

#     conn.close()








