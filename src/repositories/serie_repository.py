import json
from pathlib import Path
import sqlite3
from domain.excecoes import DadosInvalidosError, CatalogoError, ItemDuplicadoError
from domain.midias import Episodio, Serie, Temporada


class SerieRepository:

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.criar_tabela()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON;") # Faz com que se um elemento que é refenciado for apagado, o que o referencia é apagado também
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
        """Adiciona a série juntamente com uma temporada e um episódio"""

        if not serie.temporadas or not serie.temporadas[0].episodios: # Verifica se a série contém ao menos um episódio
            raise DadosInvalidosError("A série precisa conter ao menos uma temporada e um episódio para ser salva.")

        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # Verifica se uma série com mesmo título e ano já existe
            cursor.execute(
                "SELECT id FROM series WHERE titulo = ? AND ano = ?",
                (serie.titulo, serie.ano),
            )
            if cursor.fetchone() is not None:
                raise ItemDuplicadoError(f"A série '{serie.titulo}' do ano {serie.ano} já existe no catálogo.")

            # Insere a Série principal e recupera o ID gerado
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
                    # Transforma os atributos que são listas em uma string json, o que torna possível guardá-las em formato texto no banco
                    json.dumps(serie.elenco, ensure_ascii=False),
                    json.dumps(serie.diretor, ensure_ascii=False),
                    json.dumps(serie.roteirista, ensure_ascii=False),
                ),
            )
            serie_id = cursor.lastrowid # serie_id é utilizada na adição das temporadas logo abaixo

            # Insere as Temporadas e seus respectivos Episódios
            for temporada in serie.temporadas:
                cursor.execute(
                    "INSERT INTO temporadas (serie_id, numero) VALUES (?, ?)",
                    (serie_id, temporada.numero),
                )
                temporada_id = cursor.lastrowid # temporada_id é utilizada na adição dos episódios logo abaixo

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
                            # Transforma os atributos que são listas em uma string json, o que torna possível guardá-las em formato texto no banco
                            json.dumps(ep.elenco, ensure_ascii=False),
                            json.dumps(ep.diretor, ensure_ascii=False),
                            json.dumps(ep.roteirista, ensure_ascii=False),
                        ),
                    )

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
                            # elenco, diretor e roteirista voltam ao formato original
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
                    # elenco, diretor e roteirista voltam ao formato original
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

        from repositories.avaliacao_repository import AvaliacaoRepository

        avaliacao_repository = AvaliacaoRepository(self.caminho)
        for serie in series_objs:
            avaliacao_repository.carregar_avaliacoes(serie)
            for temporada in serie.temporadas:
                avaliacao_repository.carregar_avaliacoes(temporada)
                for episodio in temporada.episodios:
                    avaliacao_repository.carregar_avaliacoes(episodio)

        return series_objs

    def buscar_id_serie(self, titulo: str, ano: int | None = None) -> int | None:
        """
        Recebe o título e o ano da série devolve o seu id
        """
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            if ano is None:
                cursor.execute(
                    "SELECT id FROM series WHERE titulo = ?",
                    (titulo,),
                )
            else:
                cursor.execute(
                    "SELECT id FROM series WHERE titulo = ? AND ano = ?",
                    (titulo, ano),
                )

            serie = cursor.fetchone()

        return serie["id"] if serie else None

    def buscar_temporada_id(self, serie_id: int, numero: int) -> int | None:
        """
        Recebe o id da serie e o número da temporada e retorna o id da da temporada
        """
        with self.conectar() as conexao:
            row = conexao.execute(
                "SELECT id FROM temporadas WHERE serie_id = ? AND numero = ?",
                (serie_id, numero),
            ).fetchone()

        return row["id"] if row else None

    def buscar_episodio_id(self, temporada_id: int, numero: int) -> int | None:
        """
        Recebe o id da temporada e o numero do episódio e retorna o id do episódio
        """
        with self.conectar() as conexao:
            row = conexao.execute(
                "SELECT id FROM episodios WHERE temporada_id = ? AND numero = ?",
                (temporada_id, numero),
            ).fetchone()

        return row["id"] if row else None

    def adicionar_temporada(self, temporada: Temporada, serie_id: int) -> str:
        """
        Adiciona uma nova temporada à série

        Recebe uma instância de temporada e o id da serie
        """
        # Verifica se a temporada não está vazia
        if not temporada.episodios:
            raise DadosInvalidosError("A temporada precisa conter ao menos um episódio")
        
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # Verifica se a temporada já não existe
            cursor.execute(
                "SELECT id FROM temporadas WHERE serie_id = ? AND numero = ?",
                (serie_id, temporada.numero),
                )

            if cursor.fetchone() is not None:
                raise ItemDuplicadoError(f"A temporada de número {temporada.numero} já existe na série")

            cursor.execute(
                "INSERT INTO temporadas (serie_id, numero) VALUES (?, ?)",
                (serie_id, temporada.numero),
            )
            temporada_id = cursor.lastrowid # temporada_id é utilizada na adição dos episódios logo abaixo
            
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
                        # Transforma os atributos que são listas em uma string json, o que torna possível guardá-las em formato texto no banco
                        json.dumps(ep.elenco, ensure_ascii=False),
                        json.dumps(ep.diretor, ensure_ascii=False),
                        json.dumps(ep.roteirista, ensure_ascii=False),
                    )
                )

        return f"Temporada {temporada.numero} adicionada com sucesso."

    def adicionar_episodio(self, episodio: Episodio, temporada_id: int) -> str:
        """
        Adiciona uma nova temporada a determinada temporada de determinada serie

        Recebe a instância de um episódio e o id da temporada
        """
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # Verifica se o episódio já existe
            cursor.execute(
                "SELECT id FROM episodios WHERE temporada_id = ? and numero = ?",
                (temporada_id, episodio.numero)
            )

            if cursor.fetchone() is not None:
                raise ItemDuplicadoError(f"O episódio de número {episodio.numero} já existe na temporada")

            # Se o episódio ainda não existir, ele é adicionado
            cursor.execute(
                """
                INSERT INTO episodios (
                    temporada_id, titulo, duracao, ano, classificacao,
                    numero, genero, elenco, diretor, roteirista
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                (
                    temporada_id,
                    episodio.titulo,
                    episodio.duracao,
                    episodio.ano,
                    episodio.classificacao,
                    episodio.numero,
                    episodio.genero,
                     # Transforma os atributos que são listas em uma string json, o que torna possível guardá-las em formato texto no banco
                    json.dumps(episodio.elenco, ensure_ascii=False),
                    json.dumps(episodio.diretor, ensure_ascii=False),
                    json.dumps(episodio.roteirista, ensure_ascii=False),
                ),
            )

        return f"Episodio {episodio.numero} adicionado com sucesso"

    def remover_episodio(self, episodio_id: int) -> str:
        """
        Remove episódio de determinada temporada de determinada série

        Recebe o id do episódio
        """
        # Verifica se foi passado o id
        if episodio_id is None:
            raise CatalogoError("O ID do episódio não pode ser None.")

        # Verifica a existência episódio e captura o id da temporada
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT temporada_id
                FROM episodios
                WHERE id = ?
                """,
                (episodio_id,),
            )
            temporada_id = cursor.fetchone()

            if temporada_id is None:
                raise CatalogoError(
                    f"Nenhum episódio foi encontrado com o ID {episodio_id}."
                )

            # Se o episódio existir, será verificado se ele é o último episódio da temporada
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM episodios
                WHERE temporada_id = ?
                """,
                (temporada_id["temporada_id"],),
            )

            if cursor.fetchone()["total"] <= 1: # Analisar depois
                raise CatalogoError(
                    "Não é possível remover o último episódio da temporada, em vez disso remova a temporada por completo"
                )

            # Caso não caia em nenhum dos casos acima, o episódio é apagado
            conexao.execute(
                "DELETE FROM episodios WHERE id = ?",
                (episodio_id,),
            )

        return "Episódio deletado com sucesso"

    def remover_temporada(self, temporada_id : int) -> str:
        """
        Remove a temporada de determinada série

        Recebe o id da temporada
        """
        # Verifica se foi passado o id
        if temporada_id is None:
            raise CatalogoError("O ID da temporada não pode ser None.")
        
        # Verifica a existência da temporada e captura o serie_id
        with self.conectar() as conexao:
            cursor = conexao.cursor()
        
            cursor.execute(
                """
                SELECT serie_id
                FROM temporadas
                WHERE id = ?
                """,
                (temporada_id,),
            )
            serie_id = cursor.fetchone()
        
            if serie_id is None:
                raise CatalogoError(
                    f"Nenhuma temporada foi encontrada com o ID {temporada_id}."
                )
        
            # Se a temporada existir, será verificado se ela é a última temporada da serie
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM temporadas
                WHERE serie_id = ?
                """,
                (serie_id["serie_id"],),
            )
        
            if cursor.fetchone()["total"] <= 1: # Analisar depois
                raise CatalogoError(
                    "Não é possível remover a última temporada da série, para isso, remova a serie por completo"
                )
        
            # Caso não caia em nenhum dos casos acima, a temporada é apagada
            conexao.execute(
                "DELETE FROM temporadas WHERE id = ?",
                (temporada_id,),
            )
        
        return "Temporada deletado com sucesso"

    def remover_serie(self, serie_id: int) -> str:
        # Verifica se o id não é None
        if serie_id is None:
            raise CatalogoError("O ID da série não pode ser None.")
        
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            # Verifica se a série existe
            cursor.execute(
                """
                SELECT id FROM series WHERE id = ?
                """,
                (serie_id,),
            )
            if cursor.fetchone() is None:
                raise CatalogoError(f"Nenhuma série foi encontrada com id {serie_id}")

            # Se a serie existir ela é apagada
            cursor.execute(
                "DELETE FROM series WHERE id = ?",
                (serie_id,),
            )

        return "Série deletada com sucesso"
