from datetime import datetime
from pathlib import Path
import sqlite3

from domain.midias import Episodio, Filme
from domain.midia_assistida import MidiaAssistida
from repositories.filme_repository import FilmeRepository
from repositories.serie_repository import SerieRepository
from domain.excecoes import CatalogoError, DadosInvalidosError


class MidiaAssistidaRepository:
    """Persiste conclusões de filmes e episódios por usuário."""

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.filme_repository = FilmeRepository(caminho)
        self.serie_repository = SerieRepository(caminho)
        self.criar_tabela()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        return conexao

    def criar_tabela(self):
        with self.conectar() as conexao:
            conexao.execute(
                """
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
                        OR
                        (tipo_midia = 'episodio' AND episodio_id IS NOT NULL AND filme_id IS NULL)
                    )
                )
                """
            )

    def adicionar(self, registro: MidiaAssistida) -> MidiaAssistida:
        """
        Adiciona uma nova mídia assistida ao banco de dados
        """
        if not isinstance(registro, MidiaAssistida):
            raise CatalogoError("O registro deve ser uma instância de MidiaAssistida.")

        with self.conectar() as conexao:
            if isinstance(registro.midia, Filme):
                # Se for um filme, é buscado o seu id
                filme_id = self._filme_id(conexao, registro.midia)
                # A mídia assistida é inserida na tabela como filme
                conexao.execute(
                    """
                    INSERT INTO midias_assistidas
                        (usuario_id, tipo_midia, filme_id, data_assistido)
                    VALUES (?, 'filme', ?, ?)
                    """,
                    (
                        registro.usuario_id,
                        filme_id,
                        registro.data_assistido.isoformat(),
                    ),
                )
            elif isinstance(registro.midia, Episodio):
                # Se for um episódio, é buscado o seu id
                episodio_id = self._episodio_id(conexao, registro.midia)
                # A mídia é inserida na tabela como um episódio
                conexao.execute(
                    """
                    INSERT INTO midias_assistidas
                        (usuario_id, tipo_midia, episodio_id, data_assistido)
                    VALUES (?, 'episodio', ?, ?)
                    """,
                    (
                        registro.usuario_id,
                        episodio_id,
                        registro.data_assistido.isoformat(),
                    ),
                )
            else:
                raise CatalogoError("Somente filmes e episódios podem ser persistidos.")
        return registro

    @staticmethod
    def _filme_id(conexao, filme: Filme) -> int:
        """
        Retorna o id de um filme
        """
        row = conexao.execute(
            "SELECT id FROM filmes WHERE titulo = ? AND ano = ?",
            (filme.titulo, filme.ano),
        ).fetchone()
        if row is None:
            raise CatalogoError(f"O filme '{filme.titulo}' não está cadastrado.")
        return row["id"]

    @staticmethod
    def _episodio_id(conexao, episodio: Episodio) -> int:
        """
        Retorna o id de uma série
        """
        if episodio.temporada is None or episodio.serie is None:
            raise CatalogoError("O episódio deve pertencer a uma série cadastrada.")
        row = conexao.execute(
            """
            SELECT e.id FROM episodios e
            JOIN temporadas t ON t.id = e.temporada_id
            JOIN series s ON s.id = t.serie_id
            WHERE s.titulo = ? AND s.ano = ?
              AND t.numero = ? AND e.numero = ?
            """,
            (
                episodio.serie.titulo,
                episodio.serie.ano,
                episodio.temporada.numero,
                episodio.numero,
            ),
        ).fetchone()
        if row is None:
            raise CatalogoError(f"O episódio '{episodio.titulo}' não está cadastrado.")
        return row["id"]

    def listar_por_usuario(self, usuario_id: str) -> list[MidiaAssistida]:
        """
        Lista as mídias assistidas de determinado usuário
        """
        with self.conectar() as conexao:
            rows = conexao.execute(
                """
                SELECT * FROM midias_assistidas
                WHERE usuario_id = ?
                ORDER BY data_assistido DESC, id DESC
                """,
                (usuario_id,),
            ).fetchall()
        return [self._reconstruir(row) for row in rows]

    def listar_ultimas(self, usuario_id: str, limite: int = 10) -> list[MidiaAssistida]:
        """
        Lista as ultimas mídias assistidas pelo usuário
        """
        if limite <= 0:
            raise DadosInvalidosError("O limite deve ser maior que zero.")
        return self.listar_por_usuario(usuario_id)[:limite]

    def _reconstruir(self, row) -> MidiaAssistida:
        """
        Reconstrói a instância de MidiaAssistida
        """
        if row["tipo_midia"] == "filme":
            midia = self._filme_por_id(row["filme_id"])
        else:
            midia = self._episodio_por_id(row["episodio_id"])
        return MidiaAssistida(
            midia=midia,
            usuario_id=row["usuario_id"],
            data_assistido=datetime.fromisoformat(row["data_assistido"]),
        )

    def _filme_por_id(self, filme_id: int) -> Filme:
        """
        Retorna o filme através de seu id
        """
        with self.conectar() as conexao:
            row = conexao.execute(
                "SELECT titulo, ano FROM filmes WHERE id = ?", (filme_id,)
            ).fetchone()
        filmes = self.filme_repository.listar_filmes()
        for filme in filmes:
            if filme.titulo == row["titulo"] and filme.ano == row["ano"]:
                return filme
        raise CatalogoError("O filme do histórico não foi encontrado.")

    def _episodio_por_id(self, episodio_id: int) -> Episodio:
        """
        Retorna o episódio através de seu id
        """
        with self.conectar() as conexao:
            row = conexao.execute(
                """
                SELECT s.titulo AS serie_titulo, s.ano AS serie_ano,
                       t.numero AS temporada_numero, e.numero AS episodio_numero
                FROM episodios e
                JOIN temporadas t ON t.id = e.temporada_id
                JOIN series s ON s.id = t.serie_id
                WHERE e.id = ?
                """,
                (episodio_id,),
            ).fetchone()
        if row is None:
            raise CatalogoError("O episódio do histórico não foi encontrado.")
        series = self.serie_repository.listar_series()
        for serie in series:
            if serie.titulo == row["serie_titulo"] and serie.ano == row["serie_ano"]:
                for temporada in serie.temporadas:
                    if temporada.numero == row["temporada_numero"]:
                        for episodio in temporada.episodios:
                            if episodio.numero == row["episodio_numero"]:
                                return episodio
        raise CatalogoError("O episódio do histórico não foi encontrado.")


MidiasAssistidasRepository = MidiaAssistidaRepository
