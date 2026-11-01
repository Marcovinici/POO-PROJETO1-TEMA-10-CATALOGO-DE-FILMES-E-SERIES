from domain.midias import Midia
from datetime import datetime
from domain.excecoes import DadosInvalidosError

class MidiaAssistida:
    """
    Registro individual de um conteúdo consumido.
    
    Attributes:
    midia (Midia): A mídia que foi assistida
    usuario_id (int): id do usuário que assistiu a mídia
    data_assistido (datetime): data do momento em que a mídia foi assistida
    """

    def __init__(self, midia: Midia, usuario_id: str, data_assistido: datetime = None):
        self.midia = midia
        self.usuario_id = usuario_id
        self.data_assistido = data_assistido or datetime.now()

    # Getter e setter de usuario_id
    @property
    def usuario_id(self) -> str:
        return self._usuario_id
    @usuario_id.setter
    def usuario_id(self, novo_usuario_id: str):
        if isinstance(novo_usuario_id, str) and novo_usuario_id.strip(): # Verifica se foi passado um argumento str e não vazio
            self._usuario_id = novo_usuario_id
        else:
            raise DadosInvalidosError(
                "O registro deve possuir um identificador de usuário válido."
            )

    # Getter setter de midia
    @property
    def midia(self) -> Midia:
        return self._midia
    @midia.setter
    def midia(self, nova_midia: Midia):
        if isinstance(nova_midia, Midia): # Verifica se o argumento é uma instância de Midia
            self._midia = nova_midia
        else:
            raise DadosInvalidosError(
                "O registro deve ser uma instância válida de Midia."
            )

    # Getter e setter de data_assistido
    @property
    def data_assistido(self) -> datetime:
        return self._data_assistido
    @data_assistido.setter
    def data_assistido(self, nova_data: datetime):
        if isinstance(nova_data, datetime): # A data deve ser datatime
            self._data_assistido = nova_data
        else:
            raise DadosInvalidosError(
                "A data de exibição deve ser um objeto datetime."
            )