from pathlib import Path
import sqlite3
from .. domain.midias import Serie

class SerieRepository():
    def __init__ (self, caminho):
        self.caminho = Path(caminho)
        self.criar_tabela()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        return conexao

    def criar_tabela(self):
        with self.conectar() as conexao:
            conexao.execute("""
            CREATE TABLE IF NOT EXISTS serie (
            titulo TEXT NOT NULL PRIMARY KEY,
            ano INTEGER NOT NULL,
            classificacao TEXT NOT NULL,
            genero TEXT,
            elenco TEXT,
            diretor TEXT,
            roteirista TEXT
            )
            """)

    def adicionar_serie(self, serie):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT titulo FROM series WHERE titulo == ?",
                (serie.titulo)
            )
            resultado = cursor.fetchone()

        if str(resultado[0]) == serie.titulo:
            return f"O filme com o título '{serie.titulo}' já existe."

        if resultado in None:
            with self.conectar() as conexao:
                conexao.execute("""
                INSERT INTO series (titulo, ano, classificacao, genero, elenco, diretor, roteirista)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (serie.titulo, serie.ano, serie.classificacao, serie.genero, serie.elenco, serie.diretor, serie.roteirista),
                )
            return "Adição de série bem sucedida"


    def listar_series(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT * FROM series"
            )
            series = cursor.fetchall()

        return [ Serie(titulo=serie['titulo'], ano=serie['ano'], classificacao=serie['classificacao'], genero=serie['genero'], elenco=serie['elenco'], diretor=serie['diretor'], roteirista=serie['roteirista']) for serie in series]
