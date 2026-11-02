from collections.abc import Iterable
from typing import Any

from domain.midias import Filme, Serie
from domain.excecoes import DadosInvalidosError


class Relatorio:
    """
    Constrói relatórios a partir do catálogo e do histórico de um usuário.

    Attributes:
    filmes (list[Filme]): Filmes do catálogo
    series (list[Serie]): Séries do catálogo
    historico (Historico): Histórico do usuário
    """

    def __init__(self, filmes: Iterable[Filme] | Any = None, series: Iterable[Serie] | Any = None, historico: Any = None):
        # Iterable é usado para mostrar que o argumento é um interável, independente do seu tipo(lista, tuplas, dicionário)
        # Caso for passado um FilmeRepository e/ou um SerieRepository, a partir de 'obter_itens', fazendo uso de um método interno dos repositories, também é extraído todas as mídias
        self.filmes = self._obter_itens(filmes, "listar_filmes")
        self.series = self._obter_itens(series, "listar_series")
        self.historico = historico

    @staticmethod
    def _obter_itens(origem: Iterable[Any] | Any, metodo: str) -> list[Any]:
        """
        Obtem midias a partir de um iterável ou de um repository de mídia
        """
        if origem is None:
            return []
        # Se for repository, a partir de um método interno (listar_filmes() para FilmeRepository e lista_series() para SerieRepository) as mídias são capturadas
        if hasattr(origem, metodo): 
            origem = getattr(origem, metodo)()
        return list(origem)

    def tempo_total_assistido(self, multiplicador: float = 1) -> float:
        """Retorna o tempo total do histórico na unidade configurada."""
        if self.historico is None:
            return 0

        registros = getattr(self.historico, "registros", None) # Captura os registros do hstórico
        if registros is None:
            registros = getattr(self.historico, "_registros", [])

        return sum(
            registro.midia.duracao * multiplicador for registro in registros
        )

    def media_de_notas_por_genero(self) -> dict[str, float]:
        """Retorna a média das avaliações agrupada pelo gênero da mídia."""
        notas_por_genero: dict[str, list[float]] = {}

        # Desempacota os filmes e series (guardados nos atributos 'filmes' e 'series'), e os percorre guardando o gênero e a nota de cada um
        for midia in [*self.filmes, *self.series]:
            genero = getattr(midia, "genero", None)
            nota = getattr(midia, "nota_media", None)
            if genero and nota is not None:
                # Cria a chave como o gênero se ainda não houver criado e adiciona a nota no dicionário
                notas_por_genero.setdefault(genero, []).append(nota)

        # É retorando um dicionário contendo os gêneros(key) com suas respectivas notas médias(value) 
        return {
            genero: round(sum(notas) / len(notas), 1)
            for genero, notas in sorted(notas_por_genero.items())
        }

    def top_10(self) -> list[dict[str, Any]]:
        """Retorna as dez mídias com maior média de avaliações."""
        # Desempacota os itens de séries e filmes e os guarda em 'catalogo'
        catalogo = [*self.filmes, *self.series]

        # guarda todas as midias avaliadas em 'avaliadas'
        avaliadas = [midia for midia in catalogo if getattr(midia, "nota_media", None) is not None]

        # Ordena as midias por nota média (midias com mesma nota são ordenadas em ordem alfabetica)
        avaliadas.sort(key=lambda midia: (-midia.nota_media, midia.titulo.casefold()))

        return [
            {
                "titulo": midia.titulo,
                "tipo": "filme" if isinstance(midia, Filme) else "serie",
                "nota_media": midia.nota_media,
            }
            for midia in avaliadas[:10]
        ]

    def recomendados(self, nota_minima: float, limite: int = 10) -> list[dict[str, Any]]:
        """Retorna até dez mídias cuja nota atinge o mínimo configurado."""
        if limite <= 0:
            raise DadosInvalidosError("O limite de recomendações deve ser maior que zero.")

        # Carrega a lista de todas as mídias
        recomendados = [
            midia
            for midia in [*self.filmes, *self.series]
            if getattr(midia, "nota_media", None) is not None
            and midia.nota_media >= nota_minima
        ]
        # Ordena por nota (maior para menor)
        recomendados.sort(key=lambda midia: (-midia.nota_media, midia.titulo.casefold()))

        return [
            {
                "titulo": midia.titulo,
                "tipo": "filme" if isinstance(midia, Filme) else "serie",
                "nota_media": midia.nota_media,
            }
            for midia in recomendados[:limite] # o máximo de mídias retornadas é determinada pela variável limite
        ]

    def series_com_mais_eps(self) -> list[dict[str, Any]]:
        """Retorna as séries ordenadas pelo número total de episódios."""
        # Ordena as series por numero de episódios em ordem decrescente (midias com mesmo numero de episodios são ordenadas em ordem alfabética)
        series = sorted(self.series, key=lambda serie: (-serie.total_episodios, serie.titulo.casefold()))
        return [
            {
                "titulo": serie.titulo,
                "total_episodios": serie.total_episodios,
            }
            for serie in series
        ]
