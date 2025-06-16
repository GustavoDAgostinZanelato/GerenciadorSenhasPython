senhas = []
senhaMestra = "123"


def cadastrarSenha():
    senha = input("\nDigite a senha: ")
    site = input("Insira o nome do serviço: ")
    id = len(senhas)
    senhas.append({
        "Id": id,
        "Serviço": site,
        "Senha": senha
    })
    print("Senha cadastrada com sucesso! \n")


def exibirSenhas():
    if(len(senhas) == 0):
        print("\nNenhuma senha cadastrada")
    else:
        print("\nSenhas Salvas")
        for item in senhas:
            print(f"{item["Id"]} - {item["Serviço"]}: {item["Senha"]}")


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


while True:
    senha = input("Insira a senha mestra: ")
    if senha != senhaMestra:
        print("Senha inválida. Tente novamente.")
    else:
        print("Acesso autorizado\n")
        break

def main():    
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
        if op not in [1,2,3,4,5]:
            print("\nOpção Inválida. Tente novamente")
            continue

        elif op == 5:
            print("\nEncerrando...")
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