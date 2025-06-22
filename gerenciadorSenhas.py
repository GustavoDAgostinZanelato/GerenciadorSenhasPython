import sqlite3
from autenticacao import entrar, cadastrar

conn = sqlite3.connect('gerenciadorSenhas.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senhaMestra TEXT NOT NULL
);
""")

# Tabela de senhas vinculadas ao usuário
cursor.execute("""
CREATE TABLE IF NOT EXISTS senhas (
    senha_id INTEGER PRIMARY KEY AUTOINCREMENT,
    servico TEXT NOT NULL,
    senha TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
);
""")

senhas = []

def carregarSenhas(usuario_id):
    """Carrega as senhas do usuário no banco de dados."""
    conn = sqlite3.connect('gerenciadorSenhas.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT senha_id, servico, senha FROM senhas WHERE usuario_id = ?", (usuario_id,))
    resultado = cursor.fetchall()
    
    # Preenche a lista senhas com os dados do banco
    global senhas
    senhas = []
    for row in resultado:
        senhas.append({
            "Id": row[0],
            "Serviço": row[1],
            "Senha": row[2]
        })
    
    print(f"{len(senhas)} senhas carregadas com sucesso!")

def salvarSenhasNoBD(usuario_id):
    """Substitui todas as senhas no banco de dados pelos dados da lista senhas."""
    conn = sqlite3.connect('gerenciadorSenhas.db')
    cursor = conn.cursor()
    
    # Exclui todas as senhas associadas ao usuário
    cursor.execute("DELETE FROM senhas WHERE usuario_id = ?", (usuario_id,))
    
    # Insere todas as senhas presentes na lista senhas
    for senha in senhas:
        cursor.execute("""
            INSERT INTO senhas (servico, senha, usuario_id)
            VALUES (?, ?, ?)
        """, (senha['Serviço'], senha['Senha'], usuario_id))

    conn.commit()
    print("Banco de dados atualizado com as senhas mais recentes!")

def cadastrarSenha():
    senha = input("\nDigite a senha: ")
    site = input("Insira o nome do serviço: ")
    
    # Gera novo ID baseado nos IDs existentes
    novo_id = max([s['Id'] for s in senhas], default=0) + 1
    
    senhas.append({
        "Id": novo_id,
        "Serviço": site,
        "Senha": senha
    })
    print("Senha cadastrada com sucesso! \n")

def exibirSenhas():
    if len(senhas) == 0:
        print("\nNenhuma senha cadastrada")
    else:
        print("\nSenhas Salvas")
        for item in senhas:
            print(f"{item['Id']} - {item['Serviço']}: {item['Senha']}")

def excluirSenha():
    while True:
        try:
            id = int(input("Insira o ID da senha que deseja remover: "))
        except ValueError:
            print("ERRO. ID inválido!")
            continue

        senhaEncontrada = None
        for item in senhas:
            if item.get("Id") == id:
                senhaEncontrada = item
                break  # Para o loop assim que encontra

        if senhaEncontrada:
            print(f"{senhaEncontrada['Id']} - {senhaEncontrada['Serviço']}: {senhaEncontrada['Senha']}")
            while True:
                op = input("Deseja remover essa senha? (S/N): ").lower().strip()
                if op == "s":
                    senhas.remove(senhaEncontrada)
                    print("Senha deletada com sucesso\n")
                    return
                elif op == "n":
                    print("Ação cancelada\n")
                    return
                else:
                    print("Opção inválida. Digite S ou N\n")
        else:
            print("Nenhuma senha encontrada com esse ID\n")

def editarSenha():
    while True:
        try:
            id = int(input("Insira o ID da senha que deseja editar: "))
        except ValueError:
            print("ERRO. ID inválido!")
            continue

        senhaEncontrada = None
        for item in senhas:
            if item.get("Id") == id:
                senhaEncontrada = item
                break  # Para o loop assim que encontra

        if senhaEncontrada:
            print(f"{senhaEncontrada['Id']} - {senhaEncontrada['Serviço']}: {senhaEncontrada['Senha']}")
            while True:
                op = input("Deseja editar essa senha? (S/N): ").lower().strip()
                if op == "s":
                    novaSenha = input(f"Nova senha para {senhaEncontrada['Serviço']}:")
                    senhaEncontrada['Senha'] = novaSenha
                    print("Senha atualizada com sucesso\n")
                    return
                elif op == "n":
                    print("Ação cancelada\n")
                    return
                else:
                    print("Opção inválida. Digite S ou N\n")
        else:
            print("Nenhuma senha encontrada com esse ID\n")

def main():  
    while True:    
        print("=" * 25)
        print("{:^25}".format("BEM VINDO(A)"))
        print("=" * 25)
        print("1️⃣  - Entrar")
        print("2️⃣  - Criar conta")

        try:
            op = int(input("Como deseja proseguir? "))
        except ValueError:
            print("\nERRO. Valor inválido")
            continue
        if op not in [1, 2]:
            print("\nOpção Inválida. Tente novamente")
            continue

        if op == 1:
            usuario_id = entrar()
            if usuario_id is not None:
                carregarSenhas(usuario_id)
                break  
        elif op == 2:
            usuario_id = cadastrar()
            if usuario_id is not None:
                carregarSenhas(usuario_id)
                break  


    while True:    
        print("=" * 40)
        print("{:^40}".format("🔐 GERENCIADOR DE SENHAS 🔐"))
        print("=" * 40)
        print("1️⃣  - Cadastrar Nova Senha")
        print("2️⃣  - Excluir Senha")
        print("3️⃣  - Editar Senhas")
        print("4️⃣  - Mostrar Senhas")
        print("5️⃣  - Sair")
        print("=" * 40)

        try:
            op = int(input("Como deseja proseguir? "))
        except ValueError:
            print("\nERRO. Valor inválido")
            continue
        if op not in [1, 2, 3, 4, 5]:
            print("\nOpção Inválida. Tente novamente")
            continue

        elif op == 5:
            print("\nEncerrando...")
            salvarSenhasNoBD(usuario_id)  # Atualiza o banco de dados com as senhas da lista
            break

        elif op == 1:
            cadastrarSenha()

        elif op == 2:
            excluirSenha()

        elif op == 3:
            editarSenha()

        elif op == 4:
            exibirSenhas()

main()
