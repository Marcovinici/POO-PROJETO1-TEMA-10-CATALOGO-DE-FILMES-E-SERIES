from pathlib import Path
import sqlite3
import json
from domain.excecoes import CatalogoError, ItemDuplicadoError
from domain.midias import Filme

class FilmeRepository:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.criar_tabela()

    def conectar(self):
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON;") # Faz com que se um elemento que é refenciado for apagado, o que o referencia é apagado também
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

    def adicionar_filme(self, filme: Filme) -> str:
        """
        Adiciona um filme no catálogo

        Recebe uma instâcia de Filme e o adiciona no banco de dados
        """
        # Transforma os atributos que são listas em uma string json, o que torna possível guardá-las em formato texto no banco
        elenco = json.dumps(filme.elenco or [], ensure_ascii=False)
        diretor = json.dumps(filme.diretor or [], ensure_ascii=False)
        roteirista = json.dumps(filme.roteirista or [], ensure_ascii=False)

        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
            "SELECT id FROM filmes WHERE titulo = ? AND ano = ?", # Verifica se o filme já existe no banco
            (filme.titulo, filme.ano),
            )
            resultado = cursor.fetchone()

        if resultado is None: # Se o filme não for encontrado, ele é adicionado no banco
            with self.conectar() as conexao:
                conexao.execute("""
                INSERT INTO filmes (titulo, duracao, ano, classificacao, genero, elenco, diretor, roteirista)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (filme.titulo, filme.duracao, filme.ano, filme.classificacao, filme.genero, elenco, diretor, roteirista),
                )
                conexao.commit()
            return "Adição de filme bem sucedida"

        raise ItemDuplicadoError(f"O filme {filme.titulo} do ano {filme.ano} já existe no banco de dados")
    

    def listar_filmes(self) -> list[Filme]:
        """
        Lista todos os filmes presentes no banco
        """
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM filmes")
            linhas = cursor.fetchall()

        filmes = [
            Filme(
                titulo=filme["titulo"],
                duracao=filme["duracao"],
                ano=filme["ano"],
                classificacao=filme["classificacao"],
                genero=filme["genero"],
                # elenco, diretor e roteirista voltam ao formato original
                elenco=json.loads(filme["elenco"]) if filme["elenco"] else [],
                diretor=json.loads(filme["diretor"]) if filme["diretor"] else [],
                roteirista=json.loads(filme["roteirista"])
                if filme["roteirista"]
                else [],
            )
            for filme in linhas
        ]
        from repositories.avaliacao_repository import AvaliacaoRepository

        avaliacao_repository = AvaliacaoRepository(self.caminho)
        for filme in filmes:
            avaliacao_repository.carregar_avaliacoes(filme)
        return filmes

    def buscar_filme_id(self, titulo: str, ano: int | None = None) -> int | None:
        """
        Recebe o título e um ano e devolve o id referente ao filme
        """
        with self.conectar() as conexao:
            cursor = conexao.cursor()

            if ano is None:
                cursor.execute(
                    "SELECT id FROM filmes WHERE titulo = ?",
                    (titulo,),
                )
            else:
                cursor.execute(
                    "SELECT id FROM filmes WHERE titulo = ? AND ano = ?",
                    (titulo, ano),
                )

            filme = cursor.fetchone()

        return filme["id"] if filme else None

    def remover_filme(self, id: int) -> str:
        """
        Deleta da tabela de filmes o filme com id passado
        """
        if id is None:
            raise CatalogoError("id do filme foi passado como None para 'remover_filme()'")
        else:
            with self.conectar() as conexao:
                conexao.execute(
                    "DELETE FROM filmes WHERE id = ?",
                    (id,),
                )
            return "Filme deletado com sucesso"
