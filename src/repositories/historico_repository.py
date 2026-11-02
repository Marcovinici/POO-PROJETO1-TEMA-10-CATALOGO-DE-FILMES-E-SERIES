from datetime import datetime

from domain.historico import Historico
from domain.midias import Episodio, Filme
from repositories.midia_assistida_repository import MidiaAssistidaRepository


class HistoricoRepository:
    """Coordena o histórico de domínio e sua persistência."""

    def __init__(self, caminho):
        self.midias_assistidas = MidiaAssistidaRepository(caminho)

    def obter_historico(self, usuario_id: str) -> Historico:
        """
        Carrega o histórico e retorna seus registros
        """
        historico = Historico(usuario_id)
        for registro in self.midias_assistidas.listar_por_usuario(usuario_id):
            historico.adicionar_registro(registro)
        return historico

    def registrar_conclusao(self, usuario_id: str, midia: Filme | Episodio, data: datetime = None):
        """
        Registra a conclusão de uma mídia
        """
        historico = Historico(usuario_id)
        registro = historico.registrar_conclusao(midia, data)
        self.midias_assistidas.adicionar(registro)
        return registro

    def listar_ultimas(self, usuario_id: str, limite: int = 10):
        """
        Lista as últimas mídias assistidas
        """
        return self.midias_assistidas.listar_ultimas(usuario_id, limite)

    def listar_filmes_assistidos(self, usuario_id: str):
        """
        Lista os filmes assistidos
        """
        return [
            registro
            for registro in self.midias_assistidas.listar_por_usuario(usuario_id)
            if isinstance(registro.midia, Filme)
        ]

    def listar_series_assistidas(self, usuario_id: str):
        """
        Lista as séries assistidas
        """
        registros = self.midias_assistidas.listar_por_usuario(usuario_id)
        series = {}
        for registro in registros:
            # Se for um episódio e o episódio pertencer a uma série:
            if isinstance(registro.midia, Episodio) and registro.midia.serie:
                serie = registro.midia.serie
                chave = (serie.titulo, serie.ano) # É guaradado o título e o ano da serie
                series[chave] = serie
        return list(series.values())

    def listar_series_em_andamento(self, usuario_id: str):
        """
        Lista as séries que estão em andamento
        """
        assistidas = self.listar_series_assistidas(usuario_id)
        registros = self.midias_assistidas.listar_por_usuario(usuario_id)
        concluidos = {}
        for registro in registros:
            if isinstance(registro.midia, Episodio) and registro.midia.serie:
                serie = registro.midia.serie
                chave = (serie.titulo, serie.ano)
                # É adicionado ao dicionário o título e ano da série caso já não tenha sido passado e é adicionado como valor o episodio assistido (numero)
                concluidos.setdefault(chave, set()).add(
                    (registro.midia.temporada.numero, registro.midia.numero)
                )

        # É retornado uma lista contendo apenas as séries não concluídas
        return [
            serie
            for serie in assistidas
            if len(concluidos[(serie.titulo, serie.ano)]) < serie.total_episodios
        ]