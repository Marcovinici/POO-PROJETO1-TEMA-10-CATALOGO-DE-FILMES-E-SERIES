from pathlib import Path
from typing import Any

from domain.relatorios import Relatorio
from repositories.filme_repository import FilmeRepository
from repositories.historico_repository import HistoricoRepository
from repositories.serie_repository import SerieRepository
from repositories.config_repository import ConfigRepository


class RelatorioRepository:
    """
    Fornece relatórios a partir dos dados persistidos do catálogo.

    Relatórios são informações derivadas; por isso, nenhuma tabela adicional é
    criada. Os cálculos permanecem na classe de domínio 'Relatorio'.
    """

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.filmes = FilmeRepository(caminho)
        self.series = SerieRepository(caminho)
        self.historico = HistoricoRepository(caminho)
        self.configuracao = ConfigRepository(self.caminho.parent / "config.json")

    def obter_relatorio(self, usuario_id: str) -> Relatorio:
        """
        Monta um relatório usando o catálogo e o histórico do usuário.
        """
        return Relatorio(
            filmes=self.filmes,
            series=self.series,
            historico=self.historico.obter_historico(usuario_id),
        )

    def tempo_total_assistido(self, usuario_id: str) -> int:
        """
        Relatório que exibe o tempo total assistido no catálogo
        """
        return self.obter_relatorio(usuario_id).tempo_total_assistido(self.configuracao.multiplicador_de_duracao)

    def media_de_notas_por_genero(self) -> dict[str, float]:
        """
        Relatório que exibe a média de notas por gênero
        """
        return self._relatorio_sem_usuario().media_de_notas_por_genero()

    def top_10(self) -> list[dict[str, Any]]:
        """
        Relatório que exibe as 10 mídias com melhor nota média
        """
        return self._relatorio_sem_usuario().top_10()

    def recomendados(self, nota_minima: float, limite: int = 10) -> list[dict[str, Any]]:
        """
        Exibe os Recomendados
        """
        return self._relatorio_sem_usuario().recomendados(nota_minima, limite)

    def series_com_mais_eps(self) -> list[dict[str, Any]]:
        """
        Relatório das séries com mais episódios
        """
        return self._relatorio_sem_usuario().series_com_mais_eps()

    def gerar_relatorios(self, usuario_id: str) -> dict[str, Any]:
        """Retorna todos os relatórios disponíveis em uma única operação."""
        relatorio = self.obter_relatorio(usuario_id)
        return {
            "tempo_total_assistido": relatorio.tempo_total_assistido(
                self.configuracao.multiplicador_de_duracao
            ),
            "media_de_notas_por_genero": relatorio.media_de_notas_por_genero(),
            "top_10": relatorio.top_10(),
            "series_com_mais_eps": relatorio.series_com_mais_eps(),
        }

    def _relatorio_sem_usuario(self) -> Relatorio:
        """
        Cria um relatório que abrange todos os usuários
        """
        return Relatorio(filmes=self.filmes, series=self.series)
