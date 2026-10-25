from pathlib import Path
import sqlite3
from ..domain.midias import Filme

class FilmeRepository:
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
            CREATE TABLE IF NOT EXISTS filmes (
                titulo TEXT NOT NULL PRIMARY KEY,
                duracao INT NOT NULL,
                ano INTEGER NOT NULL,
                classificacao TEXT NOT NULL,
                genero TEXT,
                elenco TEXT,
                diretor TEXT,
                roteirista TEXT
                )
            """)

    def adicionar_filme(self, filme):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            "SELECT titulo FROM filmes WHERE titulo == ?",
            (filme.titulo)
            )
            resultado = cursor.fetchone()

        if str(resultado[0]) == filme.titulo:
            return f"O filme com o título '{filme.titulo}' já existe."

        if resultado is None:
            with self.conectar() as conexao:
                conexao.execute("""
                INSERT INTO filmes (titulo, duracao, ano, classificacao, genero, elenco, diretor, roteirista)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (filme.titulo, filme.duracao, filme.ano, filme.classificacao, filme.genero, filme.elenco, filme.diretor, filme.roteirista),
                )
            return "Adição de filme bem sucedida"
    

    def listar_filmes(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT * FROM filmes"
            )
            filmes = cursor.fetchall()

        return [Filme(titulo=filme['titulo'], duracao=filme['duracao'], ano=filme['ano'], classificacao=filme['classificacao'], genero=filme['genero'], elenco=filme['elenco'], diretor=filme['diretor'], roteirista=filme['roteirista']) for filme in filmes]
