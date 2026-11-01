import sqlite3
from pathlib import Path
import json
from domain.listas import ListaPersonalizada
from domain.midias import Filme, Serie, Temporada, Episodio


class ListasRepository:

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.criar_tabelas()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao

    def _json_para_lista(self, texto: str | None) -> list[str]:
        if not texto:
            return []

        resultado = json.loads(texto)

        if not isinstance(resultado, list):
            raise ValueError("O valor persistido deve representar uma lista JSON.")

        return resultado

    def criar_tabelas(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.executescript("""
                -- Tabela principal de listas do usuário
                CREATE TABLE IF NOT EXISTS listas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    usuario_id TEXT NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(nome_de_usuario) ON DELETE CASCADE,
                    UNIQUE(nome, usuario_id)
                );

                -- Tabela intermediária usando os títulos como chave estrangeira
                CREATE TABLE IF NOT EXISTS lista_midia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lista_id INTEGER NOT NULL,
                    filme_id INTEGER,
                    serie_id INTEGER,
                    FOREIGN KEY (lista_id) REFERENCES listas(id) ON DELETE CASCADE,
                    FOREIGN KEY (filme_id) REFERENCES filmes(id) ON DELETE CASCADE,
                    FOREIGN KEY (serie_id) REFERENCES series(id) ON DELETE CASCADE,
                    CHECK (
                        (filme_id IS NOT NULL AND serie_id IS NULL) OR
                        (filme_id IS NULL AND serie_id IS NOT NULL)
                    ),
                    UNIQUE(lista_id, filme_id, serie_id)
                );
            """)

    # --- OPERAÇÕES NA TABELA 'listas' ---

    def criar_lista(self, nome: str, usuario_id: str):
        """Cria uma nova lista associada ao nome do usuário e retorna o ID gerado."""
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO listas (nome, usuario_id) VALUES (?, ?)",
                (nome, usuario_id),
            )
            conexao.commit()
            return cursor.lastrowid

    def listar_listas_por_usuario(self, usuario_id: str):
        """Retorna todas as listas cadastradas por um determinado usuário."""
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT * FROM listas WHERE usuario_id = ?", (usuario_id,)
            )
            rows = cursor.fetchall()

            return [
                ListaPersonalizada(
                    nome_da_lista=row["nome"],
                    usuario=row["usuario_id"],
                    id=row["id"],
                )
                for row in rows
            ]

    def buscar_id_por_nome(
        self, nome_da_lista: str, usuario_id: str
    ) -> int | None:
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id FROM listas WHERE nome = ? AND usuario_id = ?",
                (nome_da_lista, usuario_id),
            )
            row = cursor.fetchone()
            return row["id"] if row else None

    # --- OPERAÇÕES NA TABELA INTERMEDIÁRIA 'lista_midia' ---

    def adicionar_filme_na_lista(self, lista_id: int, filme_id: int):
        """Associa um filme à lista usando o título do filme."""
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO lista_midia (lista_id, filme_id, serie_id)
                VALUES (?, ?, NULL)
            """,
                (lista_id, filme_id),
            )
            conexao.commit()

    def adicionar_serie_na_lista(self, lista_id: int, serie_id: int):
        """Associa uma série à lista usando o título da série."""
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO lista_midia (lista_id, filme_id, serie_id)
                VALUES (?, NULL, ?)
            """,
                (lista_id, serie_id),
            )
            conexao.commit()

    def _carregar_serie(self, cursor, serie_id: int) -> Serie | None:
        cursor.execute(
            "SELECT * FROM series WHERE id = ?",
            (serie_id,),
        )
        serie_row = cursor.fetchone()

        if serie_row is None:
            return None

        cursor.execute(
            """
            SELECT *
            FROM temporadas
            WHERE serie_id = ?
            ORDER BY numero
            """,
            (serie_id,),
        )
        temporada_rows = cursor.fetchall()

        temporadas = []

        for temporada_row in temporada_rows:
            cursor.execute(
                """
                SELECT *
                FROM episodios
                WHERE temporada_id = ?
                ORDER BY numero
                """,
                (temporada_row["id"],),
            )
            episodio_rows = cursor.fetchall()

            episodios = [
                Episodio(
                    titulo=row["titulo"],
                    duracao=row["duracao"],
                    ano=row["ano"],
                    classificacao=row["classificacao"],
                    numero=row["numero"],
                    genero=row["genero"],
                    elenco=self._json_para_lista(row["elenco"]),
                    diretor=self._json_para_lista(row["diretor"]),
                    roteirista=self._json_para_lista(row["roteirista"]),
                )
                for row in episodio_rows
            ]

            temporadas.append(
                Temporada(
                    numero=temporada_row["numero"],
                    episodios=episodios,
                )
            )

        return Serie(
            titulo=serie_row["titulo"],
            ano=serie_row["ano"],
            classificacao=serie_row["classificacao"],
            genero=serie_row["genero"],
            elenco=self._json_para_lista(serie_row["elenco"]),
            diretor=self._json_para_lista(serie_row["diretor"]),
            roteirista=self._json_para_lista(serie_row["roteirista"]),
            temporadas=temporadas,
        )

    def remover_filme_da_lista(self, lista_id: int, filme_id: int):
        """Remove a associação de um filme com a lista."""
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                DELETE FROM lista_midia
                WHERE lista_id = ? AND filme_id = ?
            """,
                (lista_id, filme_id),
            )
            conexao.commit()

    def remover_serie_da_lista(self, lista_id: int, serie_id: int):
        """Remove a associação de uma série com a lista."""
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                DELETE FROM lista_midia
                WHERE lista_id = ? AND serie_id = ?
            """,
                (lista_id, serie_id),
            )
            conexao.commit()

    # --- MONTAGEM DO OBJETO COMPLETO DO DOMAIN ---

    def obter_lista_com_midias(self, lista_id: int):
        """Recupera a lista do banco montando as instâncias de Filme e Serie."""
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # 1. Busca os dados da lista
            cursor.execute("SELECT * FROM listas WHERE id = ?", (lista_id,))
            row_lista = cursor.fetchone()
            if not row_lista:
                return None

            lista_obj = ListaPersonalizada(
                nome_da_lista=row_lista["nome"],
                usuario=row_lista["usuario_id"],
                id=row_lista["id"],
            )

            # 2. Carrega todos os FILMES vinculados (JOIN usando titulo)
            cursor.execute(
                """
                SELECT f.* FROM filmes f
                JOIN lista_midia lm ON f.id = lm.filme_id
                WHERE lm.lista_id = ?
            """,
                (lista_id,),
            )
            for row in cursor.fetchall():
                filme = Filme(
                    titulo=row["titulo"],
                    duracao=row["duracao"],
                    ano=row["ano"],
                    classificacao=row["classificacao"],
                    genero=row["genero"],
                    elenco=self._json_para_lista(row["elenco"]),
                    diretor=self._json_para_lista(row["diretor"]),
                    roteirista=self._json_para_lista(row["roteirista"]),
                )
                lista_obj.adicionar_na_lista(filme)

            # 3. Carrega todas as SÉRIES vinculadas (JOIN usando titulo)
            cursor.execute(
                """
                SELECT s.* FROM series s
                JOIN lista_midia lm ON s.id = lm.serie_id
                WHERE lm.lista_id = ?
            """,
                (lista_id,),
            )
            for row in cursor.fetchall():
                serie = self._carregar_serie(cursor, row["id"])

                if serie is not None:
                    lista_obj.adicionar_na_lista(serie)

            return lista_obj