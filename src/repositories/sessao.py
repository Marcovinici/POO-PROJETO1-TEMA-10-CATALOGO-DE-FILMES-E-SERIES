from pathlib import Path
import sqlite3
from ..domain.usuario import Usuario

class Sessao:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.criar_tabela()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao

    def criar_tabela(self):
        with self.conectar() as conexao:
            conexao.execute("""
            CREATE TABLE IF NOT EXISTS sessao(
            id INTEGER PRIMARY KEY CHECK (id = 1),
            nome_de_usuario TEXT NOT NULL,
            FOREIGN KEY (nome_de_usuario) REFERENCES usuarios(nome_de_usuario) ON DELETE CASCADE
            );
            """)
    
    def registrar_login(self, nome_de_usuario):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO sessao (id, nome_de_usuario)
            VALUES(1, ?)
            """,
            (nome_de_usuario,),
            )

    def encerrar_sessao(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
            DELETE FROM sessao;
            """)

    def obter_usuario_logado(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
            SELECT usuarios.* FROM usuarios
            JOIN sessao atual ON usuarios.nome_de_usuario = atual.nome_de_usuario
            WHERE atual.id = 1
            """)

            user = cursor.fetchone()
            if not user:
                return None

            return Usuario(
                nome_de_usuario=user["nome_de_usuario"],
                senha=user["senha"],
                nome=user["nome"],
                tipo=user["tipo"],
            )
