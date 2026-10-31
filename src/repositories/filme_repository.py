from pathlib import Path
import sqlite3
import json
from domain.midias import Filme

class FilmeRepository:
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
            CREATE TABLE IF NOT EXISTS filmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                duracao INT NOT NULL,
                ano INTEGER NOT NULL,
                classificacao TEXT NOT NULL,
                genero TEXT,
                elenco TEXT,
                diretor TEXT,
                roteirista TEXT,
                UNIQUE(titulo, ano)
                )
            """)

    def adicionar_filme(self, filme: Filme):
        elenco = json.dumps(filme.elenco or [], ensure_ascii=False)
        diretor = json.dumps(filme.diretor or [], ensure_ascii=False)
        roteirista = json.dumps(filme.roteirista or [], ensure_ascii=False)

        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            "SELECT id FROM filmes WHERE titulo = ? AND ano = ?",
            (filme.titulo, filme.ano),
            )
            resultado = cursor.fetchone()

        if resultado is None:
            with self.conectar() as conexao:
                conexao.execute("""
                INSERT INTO filmes (titulo, duracao, ano, classificacao, genero, elenco, diretor, roteirista)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (filme.titulo, filme.duracao, filme.ano, filme.classificacao, filme.genero, elenco, diretor, roteirista),
                )
                conexao.commit()
            return "Adição de filme bem sucedida"

        return f"O filme com o título '{filme.titulo}' do ano {filme.ano} já existe."
    

    def listar_filmes(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM filmes")
            filmes = cursor.fetchall()

        return [
            Filme(
                titulo=filme["titulo"],
                duracao=filme["duracao"],
                ano=filme["ano"],
                classificacao=filme["classificacao"],
                genero=filme["genero"],
                elenco=json.loads(filme["elenco"]) if filme["elenco"] else [],
                diretor=json.loads(filme["diretor"]) if filme["diretor"] else [],
                roteirista=json.loads(filme["roteirista"])
                if filme["roteirista"]
                else [],
            )
            for filme in filmes
        ]