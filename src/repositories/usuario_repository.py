from pathlib import Path
import sqlite3

class UsuarioRepository:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.criar_tabela()


    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        return conexao


    def criar_tabela(self):
        with self.conectar() as conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    nome_de_usuario VARCHAR(100) PRIMARY KEY,
                    senha INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    tipo TEXT NOT NULL
                    )
                """)


    def existe_usuario(self, nome_de_usuario):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                SELECT nome_de_usuario FROM usuarios 
                """
            )
            nomes = cursor.fetchall()

        # Verificando existencia do usuário
        for nome in nomes:
            if str(nome[0]).strip() == str(nome_de_usuario).strip():
                return True
        return False


    def senha_verificada(self, nome_usuario, senha):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT senha FROM usuarios WHERE nome_de_usuario = ?",
                (nome_usuario.strip(),),
            )
            senha_do_banco = cursor.fetchone()

        if senha_do_banco is None:
            return False
        
        if str(senha).strip() == str(senha_do_banco[0]).strip():
            return True
        return False


    def cadastrar(self, usuario):
        if self.existe_usuario(usuario.nome_de_usuario):
            return f"O usuário {usuario.nome_de_usuario} já existe no banco de dados, faça o login"
            
        with self.conectar() as conexao:
            conexao.execute(
                "INSERT INTO usuarios (nome_de_usuario, senha, nome, tipo) VALUES (?, ?, ?, ?)",
                (usuario.nome_de_usuario, usuario.senha, usuario.nome, usuario.tipo),
            )

        return "Cadastro bem sucedido"

    def login(self, nome_usuario, senha):
        if self.existe_usuario(nome_usuario) and self.senha_verificada(nome_usuario, senha):
            return f"Bem vindo ao Catálogo de Midias CLI, {nome_usuario}"
        else:
            return "Usuário e/ou senha incorreto(s), se ainda não tem um usuário cadastre-se"
