from pathlib import Path
import sqlite3
from domain.midias import Serie

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
            CREATE TABLE IF NOT EXISTS series (
            titulo TEXT NOT NULL PRIMARY KEY,
            ano INTEGER NOT NULL,
            classificacao TEXT NOT NULL,
            genero TEXT,
            elenco TEXT,
            diretor TEXT,
            roteirista TEXT
            )
            """)

    def adicionar_serie(self, serie: Serie):
        elenco = ", ".join(serie.elenco) if isinstance(serie.elenco, list) else serie.elenco or ""
        diretor = ", ".join(serie.diretor) if isinstance(serie.diretor, list) else serie.diretor or ""
        roteirista = ", ".join(serie.roteirista) if isinstance(serie.roteirista, list) else serie.roteirista or ""

        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT titulo FROM series WHERE titulo == ?",
                (serie.titulo,)
            )
            resultado = cursor.fetchone()

        if resultado is None:
            with self.conectar() as conexao:
                conexao.execute("""
                INSERT INTO series (titulo, ano, classificacao, genero, elenco, diretor, roteirista)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (serie.titulo, serie.ano, serie.classificacao, serie.genero, elenco, diretor, roteirista),
                )
                conexao.commit()
            return "Adição de série bem sucedida"
        
        return f"O serie com o título '{serie.titulo}' já existe."


    def listar_series(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT * FROM series"
            )
            series = cursor.fetchall()

        return [ Serie(titulo=serie['titulo'], ano=serie['ano'], classificacao=serie['classificacao'], genero=serie['genero'], elenco=str(serie['elenco']).split(", "), diretor=str(serie['diretor']).split(", "), roteirista=str(serie['roteirista']).split(", ")) for serie in series]
