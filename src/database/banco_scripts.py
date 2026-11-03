"""Cria o banco SQLite e insere dados de demonstração.

O script pode ser executado várias vezes sem duplicar os dados de exemplo.
A tabela ``sessao`` é criada, mas permanece vazia.
"""

from datetime import datetime
from pathlib import Path
import json
import sqlite3
from datetime import timedelta


CAMINHO = Path(__file__).with_name("banco.db")


def conectar():
    conexao = sqlite3.connect(CAMINHO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas(conexao):
    conexao.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            nome_de_usuario TEXT PRIMARY KEY,
            senha TEXT NOT NULL,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('PADRAO', 'ADMIN'))
        );

        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            duracao INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            classificacao TEXT NOT NULL,
            genero TEXT,
            elenco TEXT,
            diretor TEXT,
            roteirista TEXT,
            UNIQUE(titulo, ano)
        );

        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            classificacao TEXT NOT NULL,
            genero TEXT,
            elenco TEXT,
            diretor TEXT,
            roteirista TEXT,
            UNIQUE(titulo, ano)
        );

        CREATE TABLE IF NOT EXISTS temporadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serie_id INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            FOREIGN KEY(serie_id) REFERENCES series(id) ON DELETE CASCADE,
            UNIQUE(serie_id, numero)
        );

        CREATE TABLE IF NOT EXISTS episodios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temporada_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            duracao INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            classificacao TEXT NOT NULL,
            numero INTEGER NOT NULL,
            genero TEXT,
            elenco TEXT,
            diretor TEXT,
            roteirista TEXT,
            FOREIGN KEY(temporada_id) REFERENCES temporadas(id) ON DELETE CASCADE,
            UNIQUE(temporada_id, numero)
        );

        CREATE TABLE IF NOT EXISTS listas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario_id TEXT NOT NULL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(nome_de_usuario)
                ON DELETE CASCADE,
            UNIQUE(nome, usuario_id)
        );

        CREATE TABLE IF NOT EXISTS lista_midia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lista_id INTEGER NOT NULL,
            filme_id INTEGER,
            serie_id INTEGER,
            FOREIGN KEY(lista_id) REFERENCES listas(id) ON DELETE CASCADE,
            FOREIGN KEY(filme_id) REFERENCES filmes(id) ON DELETE CASCADE,
            FOREIGN KEY(serie_id) REFERENCES series(id) ON DELETE CASCADE,
            CHECK (
                (filme_id IS NOT NULL AND serie_id IS NULL)
                OR (filme_id IS NULL AND serie_id IS NOT NULL)
            ),
            UNIQUE(lista_id, filme_id, serie_id)
        );

        CREATE TABLE IF NOT EXISTS midias_assistidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT NOT NULL,
            tipo_midia TEXT NOT NULL CHECK(tipo_midia IN ('filme', 'episodio')),
            filme_id INTEGER,
            episodio_id INTEGER,
            data_assistido TEXT NOT NULL,
            FOREIGN KEY(filme_id) REFERENCES filmes(id) ON DELETE CASCADE,
            FOREIGN KEY(episodio_id) REFERENCES episodios(id) ON DELETE CASCADE,
            CHECK (
                (tipo_midia = 'filme' AND filme_id IS NOT NULL AND episodio_id IS NULL)
                OR (tipo_midia = 'episodio' AND episodio_id IS NOT NULL AND filme_id IS NULL)
            )
        );

        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL
                CHECK(tipo IN ('Filme', 'Serie', 'Temporada', 'Episodio')),
            usuario TEXT NOT NULL,
            nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 10),
            comentario TEXT,
            filme_id INTEGER,
            serie_id INTEGER,
            temporada_id INTEGER,
            episodio_id INTEGER,
            FOREIGN KEY(filme_id) REFERENCES filmes(id) ON DELETE CASCADE,
            FOREIGN KEY(serie_id) REFERENCES series(id) ON DELETE CASCADE,
            FOREIGN KEY(temporada_id) REFERENCES temporadas(id) ON DELETE CASCADE,
            FOREIGN KEY(episodio_id) REFERENCES episodios(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS sessao (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            nome_de_usuario TEXT NOT NULL,
            FOREIGN KEY(nome_de_usuario) REFERENCES usuarios(nome_de_usuario)
                ON DELETE CASCADE
        );
        """
    )


def serializar_lista(valor):
    return json.dumps(valor, ensure_ascii=False)


def inserir_dados(conexao):
    usuarios = [
        ("admin", "admin123", "Administrador", "ADMIN"),
        ("ana", "ana12345", "Ana Souza", "PADRAO"),
        ("bruno", "bruno123", "Bruno Lima", "PADRAO"),
        ("carla", "carla123", "Carla Mendes", "PADRAO"),
    ]
    conexao.executemany(
        """
        INSERT OR IGNORE INTO usuarios (nome_de_usuario, senha, nome, tipo)
        VALUES (?, ?, ?, ?)
        """,
        usuarios,
    )

    filmes = [
        ("Interestelar", 169, 2014, "LIVRE", "Ficção científica"),
        ("O Poderoso Chefão", 175, 1972, "LIVRE", "Drama"),
        ("Parasita", 132, 2019, "LIVRE", "Drama"),
        ("Homem-Aranha no Aranhaverso", 117, 2018, "LIVRE", "Animação"),
        ("A Viagem de Chihiro", 125, 2001, "LIVRE", "Fantasia"),
        ("Matrix", 136, 1999, "LIVRE", "Ação"),
    ]
    for titulo, duracao, ano, classificacao, genero in filmes:
        conexao.execute(
            """
            INSERT OR IGNORE INTO filmes
                (titulo, duracao, ano, classificacao, genero, elenco, diretor, roteirista)
            VALUES (?, ?, ?, ?, ?, '[]', '[]', '[]')
            """,
            (titulo, duracao, ano, classificacao, genero),
        )

    series = [
        (
            "Ruptura", 2022, "LIVRE", "Ficção científica",
            [(1, [
                ("Boas notícias", 52, 2022, 1),
                ("Metade do laço", 48, 2022, 2),
            ])],
        ),
        (
            "The Office", 2005, "LIVRE", "Comédia",
            [(1, [
                ("Pilot", 22, 2005, 1),
                ("Diversity Day", 22, 2005, 2),
                ("Health Care", 22, 2005, 3),
            ])],
        ),
        (
            "The Last of Us", 2023, "LIVRE", "Drama",
            [(1, [
                ("When You're Lost in the Darkness", 81, 2023, 1),
                ("Infected", 53, 2023, 2),
            ])],
        ),
    ]

    for titulo, ano, classificacao, genero, temporadas in series:
        conexao.execute(
            """
            INSERT OR IGNORE INTO series
                (titulo, ano, classificacao, genero, elenco, diretor, roteirista)
            VALUES (?, ?, ?, ?, '[]', '[]', '[]')
            """,
            (titulo, ano, classificacao, genero),
        )
        serie_id = conexao.execute(
            "SELECT id FROM series WHERE titulo = ? AND ano = ?",
            (titulo, ano),
        ).fetchone()[0]

        for numero_temporada, episodios in temporadas:
            conexao.execute(
                """
                INSERT OR IGNORE INTO temporadas (serie_id, numero)
                VALUES (?, ?)
                """,
                (serie_id, numero_temporada),
            )
            temporada_id = conexao.execute(
                """
                SELECT id FROM temporadas
                WHERE serie_id = ? AND numero = ?
                """,
                (serie_id, numero_temporada),
            ).fetchone()[0]
            for titulo_ep, duracao, ano_ep, numero_ep in episodios:
                conexao.execute(
                    """
                    INSERT OR IGNORE INTO episodios
                        (temporada_id, titulo, duracao, ano, classificacao,
                         numero, genero, elenco, diretor, roteirista)
                    VALUES (?, ?, ?, ?, 'LIVRE', ?, ?, '[]', '[]', '[]')
                    """,
                    (
                        temporada_id, titulo_ep, duracao, ano_ep, numero_ep,
                        genero,
                    ),
                )

    ids_filmes = {
        titulo: conexao.execute(
            "SELECT id FROM filmes WHERE titulo = ? AND ano = ?",
            (titulo, ano),
        ).fetchone()[0]
        for titulo, _, ano, _, _ in filmes
    }
    ids_series = {
        titulo: conexao.execute(
            "SELECT id FROM series WHERE titulo = ? AND ano = ?",
            (titulo, ano),
        ).fetchone()[0]
        for titulo, ano, _, _, _ in series
    }

    listas = [
        ("Favoritos da Ana", "ana"),
        ("Para assistir", "ana"),
        ("Clássicos", "bruno"),
        ("Séries em destaque", "carla"),
    ]
    conexao.executemany(
        "INSERT OR IGNORE INTO listas (nome, usuario_id) VALUES (?, ?)",
        listas,
    )
    lista_ids = {
        nome: conexao.execute(
            "SELECT id FROM listas WHERE nome = ? AND usuario_id = ?",
            (nome, usuario),
        ).fetchone()[0]
        for nome, usuario in listas
    }
    relacoes = [
        ("Favoritos da Ana", ids_filmes["Interestelar"], None),
        ("Favoritos da Ana", ids_filmes["Parasita"], None),
        ("Clássicos", ids_filmes["O Poderoso Chefão"], None),
        ("Para assistir", ids_filmes["A Viagem de Chihiro"], None),
        ("Favoritos da Ana", None, ids_series["Ruptura"]),
        ("Para assistir", None, ids_series["The Last of Us"]),
    ]
    for nome_lista, filme_id, serie_id in relacoes:
        lista_id = lista_ids[nome_lista]
        conexao.execute(
            """
            INSERT OR IGNORE INTO lista_midia (lista_id, filme_id, serie_id)
            VALUES (?, ?, ?)
            """,
            (lista_id, filme_id, serie_id),
        )

    def episodio_id(titulo_serie, numero_temporada, numero_episodio):
        serie_id = ids_series[titulo_serie]
        return conexao.execute(
            """
            SELECT e.id FROM episodios e
            JOIN temporadas t ON t.id = e.temporada_id
            WHERE t.serie_id = ? AND t.numero = ? AND e.numero = ?
            """,
            (serie_id, numero_temporada, numero_episodio),
        ).fetchone()[0]

    agora = datetime(2026, 11, 1, 12, 0)
    historico = [
        ("ana", "filme", ids_filmes["Interestelar"], None, agora - timedelta(days=1)),
        ("ana", "filme", ids_filmes["Parasita"], None, agora - timedelta(days=5)),
        ("ana", "episodio", None, episodio_id("Ruptura", 1, 1), agora - timedelta(days=2)),
        ("ana", "episodio", None, episodio_id("The Last of Us", 1, 1), agora - timedelta(days=20)),
        ("bruno", "filme", ids_filmes["Matrix"], None, agora - timedelta(days=3)),
        ("bruno", "episodio", None, episodio_id("The Office", 1, 1), agora - timedelta(days=10)),
        ("carla", "filme", ids_filmes["A Viagem de Chihiro"], None, agora - timedelta(days=45)),
    ]
    for usuario, tipo, filme_id, episodio_id_value, data in historico:
        conexao.execute(
            """
            INSERT INTO midias_assistidas
                (usuario_id, tipo_midia, filme_id, episodio_id, data_assistido)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM midias_assistidas
                WHERE usuario_id = ? AND tipo_midia = ?
                  AND filme_id IS ? AND episodio_id IS ?
            )
            """,
            (
                usuario, tipo, filme_id, episodio_id_value, data.isoformat(),
                usuario, tipo, filme_id, episodio_id_value,
            ),
        )

    avaliacoes = [
        ("Filme", "ana", 9.5, "Excelente", ids_filmes["Interestelar"], None, None, None),
        ("Filme", "bruno", 9.0, "Um clássico", ids_filmes["O Poderoso Chefão"], None, None, None),
        ("Filme", "carla", 8.5, "Muito bom", ids_filmes["Parasita"], None, None, None),
        ("Filme", "ana", 9.0, "Animação incrível", ids_filmes["A Viagem de Chihiro"], None, None, None),
        ("Filme", "bruno", 8.0, "Boa ação", ids_filmes["Matrix"], None, None, None),
        ("Serie", "ana", 9.2, "Roteiro excelente", None, ids_series["Ruptura"], None, None),
        ("Serie", "bruno", 8.7, "Muito divertida", None, ids_series["The Office"], None, None),
        ("Serie", "carla", 9.0, "Adaptação forte", None, ids_series["The Last of Us"], None, None),
    ]
    for avaliacao in avaliacoes:
        conexao.execute(
            """
            INSERT INTO avaliacoes
                (tipo, usuario, nota, comentario, filme_id, serie_id,
                 temporada_id, episodio_id)
            SELECT ?, ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM avaliacoes
                WHERE tipo = ? AND usuario = ? AND nota = ?
                  AND comentario IS ? AND filme_id IS ? AND serie_id IS ?
                  AND temporada_id IS ? AND episodio_id IS ?
            )
            """,
            (*avaliacao, *avaliacao),
        )


def main():
    CAMINHO.parent.mkdir(parents=True, exist_ok=True)
    with conectar() as conexao:
        criar_tabelas(conexao)
        inserir_dados(conexao)
        conexao.execute("DELETE FROM sessao")
    print(f"Banco de demonstração preparado em {CAMINHO}")


if __name__ == "__main__":
    main()

