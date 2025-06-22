import sqlite3

conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    nomeUsuario TEXT NOT NULL,
    senhaLogin TEXT NOT NULL,
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    );
''')



def getPassword():
    filtro = input("Filtar senhas pelo nome do serviço? S/N ").lower()
    if filtro not in ["s","n"]:
        print("Opção inválida")

    elif filtro == "s":
         service = input("Insira o nome do serviço: ")
         cursor.execute(f'''
            SELECT username, password FROM users
            WHERE service = '{service}'
        ''')   
         for user in cursor.fetchall():
             print(user)

    else:
        cursor.execute(f'''
            SELECT * FROM users
        ''')
        for user in cursor.fetchall():
            print(user)



def insertPassword(service, username, password):
    cursor.execute(f'''
        INSERT INTO users (service, username, password)
        VALUES ('{service}', '{username}', '{password}')
    ''')
    conn.commit()


def showServices():
    cursor.execute('''
        SELECT service FROM users;
        ''')
    for service in cursor.fetchall():
        print(service)


def deletePassword():
    service, password = input("Insira o nome do serviço/senha ").split("/")
    cursor.execute(f'''
                DELETE FROM users
                WHERE service = '{service}' and password = '{password}'
                   ''')
    conn.commit()
    print(f"Senha do serviço {service} deletada com sucesso")

masterPassword = "123"
while True:
    print("\nGERENCIADOR DE SENHAS")
    senha = input("Digite a senha master: ")

    if senha != masterPassword:
        print("Senha Inválida")
        continue
    else:
        break


while True:
    print("\n1-Salvar nova Senha \n2-Listar nome dos serviços Salvos \n3-Visualizar Senhas \n4-Deletar Senha \n5-Sair")
    op = int(input(""))
    if op not in [1,2,3,4,5]:
        print("Opção Inválida")
        continue

    if op == 5:
        break

    elif op == 1:
        service = input("Nome do serviço: ")
        username = input("Nome de usuário: ")
        password = input("Qual a senha: ")
        insertPassword(service, username, password)

    elif op == 2:
        showServices()

    elif op == 3:
        getPassword()

    elif op == 4:
        deletePassword()
    
conn.close()