import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Banco de Dados
conn = sqlite3.connect('gerenciadorSenhas.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute("""CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senhaMestra TEXT NOT NULL
);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS senhas (
    senha_id INTEGER PRIMARY KEY AUTOINCREMENT,
    servico TEXT NOT NULL,
    senha TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
);""")

# Funções de Banco de Dados
def carregarSenhas(usuario_id):
    cursor.execute("SELECT senha_id, servico, senha FROM senhas WHERE usuario_id = ?", (usuario_id,))
    resultado = cursor.fetchall()
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
    cursor.execute("DELETE FROM senhas WHERE usuario_id = ?", (usuario_id,))
    for senha in senhas:
        cursor.execute("""INSERT INTO senhas (servico, senha, usuario_id)
                          VALUES (?, ?, ?)""", (senha['Serviço'], senha['Senha'], usuario_id))
    conn.commit()

def cadastrarSenha():
    site = simpledialog.askstring("Novo Serviço", "Insira o nome do serviço:")  # Pergunta o serviço primeiro
    if not site:  # Verifica se o serviço foi deixado em branco
        messagebox.showerror("Erro", "O serviço não pode ser vazio!")
        return

    senha = simpledialog.askstring("Nova Senha", "Digite a senha:")  # Pergunta a senha depois
    if not senha:  # Verifica se a senha foi deixada em branco
        messagebox.showerror("Erro", "A senha não pode ser vazia!")
        return
    
    # Gera novo ID baseado nos IDs existentes
    novo_id = max([s['Id'] for s in senhas], default=0) + 1
    
    # Adiciona a senha à lista
    senhas.append({
        "Id": novo_id,
        "Serviço": site,
        "Senha": senha
    })
    
    # Mostra uma mensagem de sucesso
    messagebox.showinfo("Sucesso", "Senha cadastrada com sucesso!")

def excluirSenha():
    id = simpledialog.askinteger("Excluir Senha", "Insira o ID da senha a ser excluída:")
    senhaEncontrada = next((item for item in senhas if item["Id"] == id), None)
    if senhaEncontrada:
        resposta = messagebox.askyesno("Confirmar Exclusão", f"Deseja excluir a senha: {senhaEncontrada['Serviço']}?")
        if resposta:
            senhas.remove(senhaEncontrada)
            messagebox.showinfo("Sucesso", "Senha deletada com sucesso!")
    else:
        messagebox.showerror("Erro", "Nenhuma senha encontrada com esse ID!")

def editarSenha():
    id = simpledialog.askinteger("Editar Senha", "Insira o ID da senha a ser editada:")
    senhaEncontrada = next((item for item in senhas if item["Id"] == id), None)
    if senhaEncontrada:
        novaSenha = simpledialog.askstring("Nova Senha", f"Nova senha para {senhaEncontrada['Serviço']}:")
        senhaEncontrada['Senha'] = novaSenha
        messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
    else:
        messagebox.showerror("Erro", "Nenhuma senha encontrada com esse ID!")

def exibirSenhas():
    if not senhas:
        messagebox.showinfo("Senhas", "Nenhuma senha cadastrada.")
    else:
        senhas_texto = "\n".join([f"{item['Id']} - {item['Serviço']}: {item['Senha']}" for item in senhas])
        messagebox.showinfo("Senhas Salvas", senhas_texto)

# Tela Principal
class GerenciadorDeSenhasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Gerenciador de Senhas 🔐")
        self.root.geometry("400x300")

        self.usuario_id = None

        self.tela_login()

    def tela_login(self):
        self.clear_screen()
        
        tk.Label(self.root, text="🔐 Bem-vindo ao Gerenciador de Senhas 🔐", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self.root, text="Nome de Usuário:").pack(pady=5)
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Senha Mestra:").pack(pady=5)
        self.senha_entry = tk.Entry(self.root, show="*")
        self.senha_entry.pack(pady=5)

        # Botão de login
        tk.Button(self.root, text="Entrar", width=20, command=self.entrar).pack(pady=10)
        tk.Button(self.root, text="Criar Conta", width=20, command=self.cadastrar).pack(pady=10)

    def tela_principal(self):
        self.clear_screen()

        tk.Label(self.root, text="🔐 Gerenciador de Senhas 🔐", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Cadastrar Nova Senha", width=20, command=cadastrarSenha).pack(pady=10)
        tk.Button(self.root, text="Excluir Senha", width=20, command=excluirSenha).pack(pady=10)
        tk.Button(self.root, text="Editar Senhas", width=20, command=editarSenha).pack(pady=10)
        tk.Button(self.root, text="Mostrar Senhas", width=20, command=exibirSenhas).pack(pady=10)
        tk.Button(self.root, text="Sair", width=20, command=self.sair).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def entrar(self):
        nome_usuario = self.usuario_entry.get()
        senha_mestra = self.senha_entry.get()

        if nome_usuario and senha_mestra:
            usuario_id = self.validar_login(nome_usuario, senha_mestra)
            if usuario_id:
                carregarSenhas(usuario_id)
                self.usuario_id = usuario_id
                self.tela_principal()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def validar_login(self, nome_usuario, senha_mestra):
        cursor.execute("SELECT id FROM usuario WHERE nome = ? AND senhaMestra = ?", (nome_usuario, senha_mestra))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None

    def cadastrar(self):
        nome = simpledialog.askstring("Cadastro", "Digite seu nome:")
        senha = simpledialog.askstring("Cadastro", "Digite sua senha mestra:")
        cursor.execute("INSERT INTO usuario (nome, senhaMestra) VALUES (?, ?)", (nome, senha))
        conn.commit()
        self.usuario_id = cursor.lastrowid
        carregarSenhas(self.usuario_id)
        self.tela_principal()

    def sair(self):
        salvarSenhasNoBD(self.usuario_id)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorDeSenhasApp(root)
    root.mainloop()
