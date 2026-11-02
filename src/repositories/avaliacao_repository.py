from pathlib import Path
import sqlite3

from domain.avaliacao import Avaliacao
from domain.midias import Episodio, Filme, Serie, Temporada
from domain.excecoes import CatalogoError


class AvaliacaoRepository:
    """Persiste avaliações e as associa às mídias do catálogo."""

    # Constante que guarda os tipos de mídia
    _TIPOS = {
        Filme: ("filme_id", "Filme"),
        Serie: ("serie_id", "Serie"),
        Temporada: ("temporada_id", "Temporada"),
        Episodio: ("episodio_id", "Episodio"),
    }

    def __init__(self, caminho):
        self.caminho = Path(caminho)
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
                    FOREIGN KEY(episodio_id) REFERENCES episodios(id) ON DELETE CASCADE,
                    CHECK (
                        (tipo = 'Filme' AND filme_id IS NOT NULL AND
                            serie_id IS NULL AND temporada_id IS NULL AND episodio_id IS NULL)
                        OR
                        (tipo = 'Serie' AND serie_id IS NOT NULL AND
                            filme_id IS NULL AND temporada_id IS NULL AND episodio_id IS NULL)
                        OR
                        (tipo = 'Temporada' AND temporada_id IS NOT NULL AND
                            filme_id IS NULL AND serie_id IS NULL AND episodio_id IS NULL)
                        OR
                        (tipo = 'Episodio' AND episodio_id IS NOT NULL AND
                            filme_id IS NULL AND serie_id IS NULL AND temporada_id IS NULL)
                    )
                )
                """
            )

    def adicionar_avaliacao(self, avaliacao: Avaliacao, midia) -> Avaliacao:
        """Salva uma avaliação e a adiciona à mídia em memória."""
        if not isinstance(avaliacao, Avaliacao):
            raise CatalogoError("A avaliação deve ser uma instância de Avaliacao.")
        coluna, tipo = self._tipo_da_midia(midia) # Captura o tipo de mídia a ser trabalhada
        if avaliacao.tipo != tipo:
            raise CatalogoError(
                f"A avaliação do tipo '{avaliacao.tipo}' não corresponde à mídia."
            )

        with self.conectar() as conexao:
            midia_id = self._buscar_id(conexao, midia, coluna) # O id da mídia é guardado em midia_id
            valores = {
                "filme_id": None,
                "serie_id": None,
                "temporada_id": None,
                "episodio_id": None,
            }
            valores[coluna] = midia_id # Na tabela, somente o campo referente ao id do tipo específico é preenchido
            # A avaliação é guardada no banco
            conexao.execute(
                """
                INSERT INTO avaliacoes
                    (tipo, usuario, nota, comentario, filme_id, serie_id,
                     temporada_id, episodio_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    avaliacao.tipo,
                    avaliacao.usuario,
                    avaliacao.nota,
                    avaliacao.comentario,
                    valores["filme_id"],
                    valores["serie_id"],
                    valores["temporada_id"],
                    valores["episodio_id"],
                ),
            )

        midia.avaliar(avaliacao)# A instância da mídia recebe a instância da avaliação
        return avaliacao

    def _tipo_da_midia(self, midia):
        """
        Distingue o tipo da mídia e o retorna juntamente com o nome da sua coluna de id
        """
        for classe, dados in self._TIPOS.items():
            if isinstance(midia, classe): # Identifica o tipo da mídia
                return dados
        raise CatalogoError(
            "A mídia deve ser Filme, Serie, Temporada ou Episodio."
        )

    def _buscar_id(self, conexao, midia, coluna):
        """
        Busca o id da mídia repassada, independentemente do seu tipo
        """
        # Guarda a consulta a ser feita para cada tipo de mídia
        consultas_por_coluna = {
            "filme_id": (
                "SELECT id FROM filmes WHERE titulo = ? AND ano = ?",
                (midia.titulo, midia.ano),
            ),
            "serie_id": (
                "SELECT id FROM series WHERE titulo = ? AND ano = ?",
                (midia.titulo, midia.ano),
            ),
        }

        # Faz a consulta correspondente ao tipo da mídia
        if coluna in consultas_por_coluna: # Usa-se apenas o valor referente ao tipo da mídia repassado
            consulta, parametros = consultas_por_coluna[coluna]
            row = conexao.execute(
                consulta, parametros
            ).fetchone()

        # Se o tipo da mídia não é nem filme nem série, mas sim temporada:
        elif coluna == "temporada_id":
            if midia.episodios[0].serie is None: # Se não pertencer a uma série resulta em erro
                raise CatalogoError("A temporada deve pertencer a uma série cadastrada.")
            serie = midia.episodios[0].serie # Captura a serie a quem a temporada está associada para a realização da consulta
            row = conexao.execute(
                """
                SELECT t.id FROM temporadas t
                JOIN series s ON s.id = t.serie_id
                WHERE s.titulo = ? AND s.ano = ? AND t.numero = ?
                """,
                (serie.titulo, serie.ano, midia.numero),
            ).fetchone()

        # E se o tipo da mídia for um episódio:
        elif coluna == "episodio_id":
            if midia.temporada is None or midia.serie is None: # Não pode ser um episódio sem temporada ou série
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
                    midia.serie.titulo,
                    midia.serie.ano,
                    midia.temporada.numero,
                    midia.numero,
                ),
            ).fetchone()
        else:
            raise CatalogoError(f"Coluna de mídia inválida: {coluna}.")
        if row is None:
            raise CatalogoError("A mídia precisa estar cadastrada antes da avaliação.")

        # Retrona o id vindo da consulta correspondente
        return row["id"]

    def listar_por_midia(self, midia) -> list[Avaliacao]:
        """
        Lista todas as avalições de determinada mídia
        """
        coluna, tipo = self._tipo_da_midia(midia) # Captura o tipo da mídia a ser trabalhada
        with self.conectar() as conexao:
            midia_id = self._buscar_id(conexao, midia, coluna) # Guarda o id em midia_id

            # Captura os dados de todas as avalições de uma mídia
            rows = conexao.execute(
                f"SELECT tipo, usuario, nota, comentario FROM avaliacoes "
                f"WHERE tipo = ? AND {coluna} = ? ORDER BY id",
                (tipo, midia_id),
            ).fetchall()

        return [self._para_dominio(row) for row in rows] # Retorna as instâncias de Avaliacao

    def carregar_avaliacoes(self, midia):
        """
        Carrega as avalições existentes no banco e as armazena na lista de avaliações da mídia
        """
        avaliacoes = self.listar_por_midia(midia)
        midia._avaliacoes = []
        for avaliacao in avaliacoes:
            midia.avaliar(avaliacao)
        return avaliacoes

    @staticmethod
    def _para_dominio(row) -> Avaliacao:
        """
        Método para gerar uma instância de Avaliação com base nos dados obtidos da tabela
        """
        return Avaliacao(
            tipo=row["tipo"],
            usuario=row["usuario"],
            nota=float(row["nota"]),
            comentario=row["comentario"],
        )

    adicionar = adicionar_avaliacao
    listar = listar_por_midia
