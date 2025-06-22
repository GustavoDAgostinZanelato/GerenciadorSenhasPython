import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# Criando a tabela, se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        nomeUsuario TEXT NOT NULL,
        senhaLogin TEXT NOT NULL,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
''')

# Lista que armazenará os dados em memória
senhas = []

# Função para carregar dados do banco para a lista
def carregarDados():
    global senhas
    cursor.execute("SELECT service, username, password FROM users")
    dados = cursor.fetchall()
    senhas = [{"service": s, "username": u, "password": p} for s, u, p in dados]

    print(senhas)


# Inserir senha (salva na lista e no banco)
def insertPassword(service, username, password):
    senhas.append({"service": service, "username": username, "password": password})
    cursor.execute('''
        INSERT INTO users (nomeUsuario, senhaLogin, service, username, password)
        VALUES ('admin', '123', ?, ?, ?)
    ''', (service, username, password))
    conn.commit()

# Mostrar todos os serviços
def showServices():
    for item in senhas:
        print(f"- {item['service']}")

# Ver senhas com ou sem filtro
def getPassword():
    filtro = input("Filtrar senhas pelo nome do serviço? S/N ").lower()
    if filtro == "s":
        service = input("Nome do serviço: ")
        encontrados = [s for s in senhas if s["service"] == service]
        if encontrados:
            for item in encontrados:
                print(f"Usuário: {item['username']} | Senha: {item['password']}")
        else:
            print("Serviço não encontrado.")
    elif filtro == "n":
        for item in senhas:
            print(f"Serviço: {item['service']} | Usuário: {item['username']} | Senha: {item['password']}")
    else:
        print("Opção inválida.")

# Deletar senha (da lista e do banco)
def deletePassword():
    service = input("Nome do serviço a ser deletado: ")
    password = input("Senha para confirmar: ")

    # Remover da lista
    global senhas
    senhas = [s for s in senhas if not (s["service"] == service and s["password"] == password)]

    # Remover do banco
    cursor.execute('''
        DELETE FROM users
        WHERE service = ? AND password = ?
    ''', (service, password))
    conn.commit()
    print(f"Senha do serviço {service} deletada com sucesso.")

# === Início do programa ===
carregarDados()

masterPassword = "123"
while True:
    print("\n🔐 GERENCIADOR DE SENHAS 🔐")
    senha = input("Digite a senha master: ")

    if senha != masterPassword:
        print("❌ Senha inválida.")
    else:
        break

while True:
    print("=" * 40)
    print("1️⃣  - Salvar nova Senha")
    print("2️⃣  - Listar serviços salvos")
    print("3️⃣  - Visualizar Senhas")
    print("4️⃣  - Deletar Senha")
    print("5️⃣  - Sair")
    print("=" * 40)

    try:
        op = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida.")
        continue

    if op == 5:
        break
    elif op == 1:
        service = input("Nome do serviço: ")
        username = input("Nome de usuário: ")
        password = input("Senha: ")
        insertPassword(service, username, password)
    elif op == 2:
        showServices()
    elif op == 3:
        getPassword()
    elif op == 4:
        deletePassword()
    else:
        print("Opção inválida.")

conn.close()
