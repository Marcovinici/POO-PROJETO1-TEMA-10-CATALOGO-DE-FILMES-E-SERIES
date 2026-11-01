from datetime import datetime, timedelta
from domain.excecoes import DadosInvalidosError
from domain.midias import Episodio, Filme, Midia
from domain.midia_assistida import MidiaAssistida


class Historico:
    """Representa o histórico de mídias assistidas pelo usuário
    
        Esta classe organiza as mídias concluídas e permite exibir um relatório
        do histórico de consumo.
    
        Attributes:
        registros (list[MidiaAssistida]): Lista contendo as mídias assistidas
        usuario_id (int): id do usuário
        """

    def __init__(self, usuario_id: str):
        if not isinstance(usuario_id, str) or not usuario_id.strip():
            raise DadosInvalidosError(
                "O histórico deve possuir um identificador de usuário válido."
            )

        self.usuario_id = usuario_id
        self._registros: list[MidiaAssistida] = []

    def registrar_conclusao(self, midia: Midia, data: datetime = None) -> MidiaAssistida:
        """
        Salva no registro uma mídia assistida

        Recebe a mídia e o horário e cria um registro de uma mídia assistida, instanciando a classe MidiaAssistida e salvando em 'registros'
        """
        if not isinstance(midia, (Filme, Episodio)):
            raise DadosInvalidosError(
                "O histórico só pode registrar filmes ou episódios concluídos."
            )

        registro = MidiaAssistida(
            midia=midia,
            usuario_id=self.usuario_id,
            data_assistido=data,
        )
        self._registros.append(registro)
        return registro


    def soma_tempo_no_periodo(self, inicio: datetime, fim: datetime) -> int:
        """
        Retorna a soma do tempo assistido em um período determinado
        """
        return sum(
            registro.midia.duracao
            for registro in self._registros
            if inicio <= registro.data_assistido <= fim
        )


    def gerar_relatorio(self, agora: datetime = None) -> dict[str, int]:
        """
        Retorna um dicionário contendo o total de tempo assistido na última semana e no último mês
        """
        fim = agora or datetime.now() # O relatório é gerado com os dados mais atuais existentes

        return {
            "ultima_semana": self.soma_tempo_no_periodo(
                fim - timedelta(days=7), # Subtrai o momento atual com o momento de 7 dias atrás e captura o tempo nesse intervalo
                fim,
            ),
            "ultimo_mes": self.soma_tempo_no_periodo(
                fim - timedelta(days=30),  # Subtrai o momento atual com o momento de 30 dias atrás e captura o tempo nesse intervalo
                fim,
            ),
        }


    def mostrar_relatorio(self, agora: datetime = None) -> dict[str, int]:
        relatorio = self.gerar_relatorio(agora)

        print("RELATÓRIO DE TEMPO ASSISTIDO")
        print(f"Última semana: {relatorio['ultima_semana']} minutos")
        print(f"Último mês: {relatorio['ultimo_mes']} minutos")

        return relatorio

    