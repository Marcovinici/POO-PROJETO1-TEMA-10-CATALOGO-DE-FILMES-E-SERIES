import json
from pathlib import Path
import sqlite3
from domain.excecoes import DadosInvalidosError
from domain.midias import Episodio, Serie, Temporada


class SerieRepository:

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        # Garante a criação da pasta se não existir
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.criar_tabela()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        # Obrigatório para garantir que deletar uma série remova temporadas/episódios vinculados (CASCADE)
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao

    def criar_tabela(self):
        """Cria a estrutura relacional completa: series, temporadas e episodios."""
        with self.conectar() as conexao:
            conexao.executescript("""
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
                FOREIGN KEY (serie_id) REFERENCES series (id) ON DELETE CASCADE,
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
                FOREIGN KEY (temporada_id) REFERENCES temporadas (id) ON DELETE CASCADE,
                UNIQUE(temporada_id, numero)
            );
            """)

    def adicionar_serie(self, serie: Serie) -> str:
        """Adiciona a série juntamente com suas temporadas e episódios dentro de uma única transação."""

        if not serie.temporadas or not serie.temporadas[0].episodios:
            raise DadosInvalidosError(
                "A série precisa conter ao menos uma temporada e um episódio para ser salva."
            )

        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # 1. Verifica se a série com mesmo título e ano já existe
            cursor.execute(
                "SELECT id FROM series WHERE titulo = ? AND ano = ?",
                (serie.titulo, serie.ano),
            )
            if cursor.fetchone() is not None:
                return f"A série '{serie.titulo}' ({serie.ano}) já existe no catálogo."

            # 2. Insere a Série principal e recupera o ID gerado
            cursor.execute(
                """
                INSERT INTO series (titulo, ano, classificacao, genero, elenco, diretor, roteirista)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    serie.titulo,
                    serie.ano,
                    serie.classificacao,
                    serie.genero,
                    json.dumps(serie.elenco, ensure_ascii=False),
                    json.dumps(serie.diretor, ensure_ascii=False),
                    json.dumps(serie.roteirista, ensure_ascii=False),
                ),
            )
            serie_id = cursor.lastrowid

            # 3. Insere as Temporadas e seus respectivos Episódios
            for temporada in serie.temporadas:
                cursor.execute(
                    "INSERT INTO temporadas (serie_id, numero) VALUES (?, ?)",
                    (serie_id, temporada.numero),
                )
                temporada_id = cursor.lastrowid

                for ep in temporada.episodios:
                    cursor.execute(
                        """
                        INSERT INTO episodios (
                            temporada_id, titulo, duracao, ano, classificacao,
                            numero, genero, elenco, diretor, roteirista
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            temporada_id,
                            ep.titulo,
                            ep.duracao,
                            ep.ano,
                            ep.classificacao,
                            ep.numero,
                            ep.genero,
                            json.dumps(ep.elenco, ensure_ascii=False),
                            json.dumps(ep.diretor, ensure_ascii=False),
                            json.dumps(ep.roteirista, ensure_ascii=False),
                        ),
                    )

            # O contexto 'with' realiza o commit automático de todas as inserções
            return f"Série '{serie.titulo}' adicionada com sucesso!"

    def listar_series(self) -> list[Serie]:
        """Carrega todas as séries reconstruindo a hierarquia completa de Temporadas e Episódios."""
        series_objs = []

        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # Busca todas as séries
            cursor.execute("SELECT * FROM series")
            series_rows = cursor.fetchall()

            for s_row in series_rows:
                serie_id = s_row["id"]

                # Busca as temporadas da série
                cursor.execute(
                    "SELECT * FROM temporadas WHERE serie_id = ? ORDER BY numero",
                    (serie_id,),
                )
                temporadas_rows = cursor.fetchall()

                temporadas_objs = []
                for t_row in temporadas_rows:
                    temp_id = t_row["id"]

                    # Busca os episódios da temporada
                    cursor.execute(
                        "SELECT * FROM episodios WHERE temporada_id = ? ORDER BY numero",
                        (temp_id,),
                    )
                    episodios_rows = cursor.fetchall()

                    episodios_objs = [
                        Episodio(
                            titulo=ep["titulo"],
                            duracao=ep["duracao"],
                            ano=ep["ano"],
                            classificacao=ep["classificacao"],
                            numero=ep["numero"],
                            genero=ep["genero"],
                            elenco=json.loads(ep["elenco"])
                            if ep["elenco"]
                            else [],
                            diretor=json.loads(ep["diretor"])
                            if ep["diretor"]
                            else [],
                            roteirista=json.loads(ep["roteirista"])
                            if ep["roteirista"]
                            else [],
                        )
                        for ep in episodios_rows
                    ]

                    # Instancia a temporada com seus episódios
                    temp = Temporada(
                        numero=t_row["numero"], episodios=episodios_objs
                    )
                    temporadas_objs.append(temp)

                # Instancia a série e os setters remontam as referências reversas ep.serie/ep.temporada automaticamente
                serie = Serie(
                    titulo=s_row["titulo"],
                    ano=s_row["ano"],
                    classificacao=s_row["classificacao"],
                    genero=s_row["genero"],
                    elenco=json.loads(s_row["elenco"])
                    if s_row["elenco"]
                    else [],
                    diretor=json.loads(s_row["diretor"])
                    if s_row["diretor"]
                    else [],
                    roteirista=json.loads(s_row["roteirista"])
                    if s_row["roteirista"]
                    else [],
                    temporadas=temporadas_objs,
                )
                series_objs.append(serie)

        return series_objs