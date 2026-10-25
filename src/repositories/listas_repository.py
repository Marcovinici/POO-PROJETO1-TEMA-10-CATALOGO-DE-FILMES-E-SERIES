from pathlib import Path
import sqlite3
from ..domain.midias import Filme
from ..domain.midias import Serie
from ..domain.listas import ListaPersonalizada

class ListasRepository:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.criar_tabelas()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao

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

                -- Tabela intermediária para o relacionamento M:N (Filmes e Séries)
                CREATE TABLE IF NOT EXISTS lista_midia (
                    lista_id INTEGER NOT NULL,
                    filme_id INTEGER,
                    serie_id INTEGER,
                    PRIMARY KEY (lista_id, filme_id, serie_id),
                    FOREIGN KEY (lista_id) REFERENCES listas(id) ON DELETE CASCADE,
                    FOREIGN KEY (filme_id) REFERENCES filmes(id) ON DELETE CASCADE,
                    FOREIGN KEY (serie_id) REFERENCES series(id) ON DELETE CASCADE,
                    -- Garante que OU tem um filme_id OU tem um serie_id (nunca os dois ou nenhum)
                    CHECK (
                        (filme_id IS NOT NULL AND serie_id IS NULL) OR
                        (filme_id IS NULL AND serie_id IS NOT NULL)
                    )
                );
            """)

# --- OPERAÇÕES NA TABELA 'listas' ---

    def criar_lista(self, nome: str, usuario_id: str):
        """Cria uma nova lista associada ao nome do usuário e retorna o ID gerado."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO listas (nome, usuario_id) VALUES (?, ?)",
                (nome, usuario_id),
            )
            return cursor.lastrowid

    def listar_listas_por_usuario(self, usuario_id: str):
        """Retorna todas as listas cadastradas por um determinado usuário."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM listas WHERE usuario_id = ?", (usuario_id,)
            )
            rows = cursor.fetchall()

            return [
                ListaPersonalizada(
                    nome_da_lista=row["nome"],
                    usuario_id=row["usuario_id"],
                    id=row["id"],
                )
                for row in rows
            ]

    # --- OPERAÇÕES NA TABELA INTERMEDIÁRIA 'lista_midia' ---

    def adicionar_filme_na_lista(self, lista_id: int, filme_id: int):
        """Associa um filme à lista."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO lista_midia (lista_id, filme_id, serie_id)
                VALUES (?, ?, NULL)
            """,
                (lista_id, filme_id),
            )

    def adicionar_serie_na_lista(self, lista_id: int, serie_id: int):
        """Associa uma série à lista."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO lista_midia (lista_id, filme_id, serie_id)
                VALUES (?, NULL, ?)
            """,
                (lista_id, serie_id),
            )

    def remover_filme_da_lista(self, lista_id: int, filme_id: int):
        """Remove a associação de um filme com a lista."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM lista_midia
                WHERE lista_id = ? AND filme_id = ?
            """,
                (lista_id, filme_id),
            )

    def remover_serie_da_lista(self, lista_id: int, serie_id: int):
        """Remove a associação de uma série com a lista."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM lista_midia
                WHERE lista_id = ? AND serie_id = ?
            """,
                (lista_id, serie_id),
            )

    # --- MONTAGEM DO OBJETO COMPLETO DO DOMAIN ---

    def obter_lista_com_midias(self, lista_id: int):
        """Recupera a lista do banco montando as instâncias de Filme e Serie."""
        with self.conectar() as conn:
            cursor = conn.cursor()

            # 1. Busca os dados da lista
            cursor.execute("SELECT * FROM listas WHERE id = ?", (lista_id,))
            row_lista = cursor.fetchone()
            if not row_lista:
                return None

            lista_obj = ListaPersonalizada(
                nome_da_lista=row_lista["nome"],
                usuario_id=row_lista["usuario_id"],
                id=row_lista["id"],
            )

            # 2. Carrega todos os FILMES vinculados
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
                    ano=row["ano"],
                    classificacao=row["classificacao"],
                    genero=row["genero"],
                    elenco=row["elenco"],
                    diretor=row["diretor"],
                    roteirista=row["roteirista"],
                )
                lista_obj.adicionar_na_lista(filme)

            # 3. Carrega todas as SÉRIES vinculadas
            cursor.execute(
                """
                SELECT s.* FROM series s
                JOIN lista_midia lm ON s.id = lm.serie_id
                WHERE lm.lista_id = ?
            """,
                (lista_id,),
            )
            for row in cursor.fetchall():
                serie = Serie(
                    titulo=row["titulo"],
                    ano=row["ano"],
                    classificacao=row["classificacao"],
                    genero=row["genero"],
                    elenco=row["elenco"],
                    diretor=row["diretor"],
                    roteirista=row["roteirista"],
                )
                lista_obj.adicionar_na_lista(serie)

            return lista_obj