from .excecoes import DadosInvalidosError

class Avaliacao:
    """Representa uma avaliação de uma mídia

    Esta classe guarda a nota e o comentário associados a uma avaliação.

    Attributes:
    tipo(str): Identifica o tipo de mídia que está sendo avaliado
    usuario (str): Identifica o usuário que fez a avaliação
    comentario (str): Representa o comentário escrito pelo usuário
    nota (float): Representa a nota atribuída pelo usuário
    """
    def __init__(self, tipo: str, usuario: str, nota: float, comentario = None):
        self.tipo = tipo
        self.usuario = usuario
        self.nota = nota
        self.comentario = comentario

    # Getter e setter do tipo
    @property
    def tipo(self):
        return self._tipo
    @tipo.setter
    def tipo(self, tipo):
        if tipo in ["Filme", "Serie", "Temporada", "Episodio"]: # Verifica se o argumento do tipo é um dos tipos válidos
            self._tipo = tipo
        else:
            raise DadosInvalidosError("O tipo de uma avaliação está restrito há: 'Filme', 'Serie', 'Temporada' ou 'Episodio'")

    # Getter e setter de nota
    @property
    def nota(self):
        return self._nota
    @nota.setter
    def nota(self, nova_nota):
        if 0 <= nova_nota <= 10 and isinstance(nova_nota, float) and not isinstance(nova_nota, bool): # Verifica se o argumento de nota é um inetiro entre de 0 a 10
            self._nota = nova_nota
        else:
            raise DadosInvalidosError("A nota presente na avaliação deve ser um inteiro de 0 a 10")

    # Getter e setter de comentario
    @property
    def comentario(self):
        return self._comentario
    @comentario.setter # Verifica se o argumento é diferente de None, e caso for do tipo 'str', comentario receberá o argumento 
    def comentario(self, novo_comentario):
        if novo_comentario is None:
            self._comentario = None
        elif isinstance(novo_comentario, str):
            if len(novo_comentario) > 0 and len(novo_comentario) > novo_comentario.count(" "):
                self._comentario = novo_comentario
            else:
                raise DadosInvalidosError("O novo comentário não pode ser vazio")
        else:
            raise DadosInvalidosError("O novo comentário deve ser do tipo 'str'")

        
    def alterar_nota(self, nova_nota: float):
        self.nota = nova_nota

    def alterar_comentario(self, novo_comentario: str):
        self.comentario = novo_comentario