class Avaliacao:
    """Representa uma avaliação de uma mídia

    Esta classe guarda a nota e o comentário associados a uma avaliação.

    Attributes:
    usuario (str): Identifica o usuário que fez a avaliação
    comentario (str): Representa o comentário escrito pelo usuário
    nota (float): Representa a nota atribuída pelo usuário
    """
    def __init__(self, tipo, usuario, nota, comentario = None):
        self.tipo = tipo
        self.usuario = usuario
        self.nota = nota
        self.comentario = comentario

    @property
    def tipo(self):
        return self._tipo
    @tipo.setter
    def tipo(self, tipo):
        if tipo in ["Filme", "Serie", "Temporada", "Episodio"]:
            self._tipo = tipo
        else:
            raise ValueError("O tipo de uma avaliação está restrito há: 'Filme', 'Serie', 'Temporada' ou 'Episodio'")

    @property
    def nota(self):
        return self._nota
    @nota.setter
    def nota(self, nova_nota):
        if 0 <= nova_nota <= 10:
            self._nota = nova_nota
        else:
            raise ValueError("A nota presente na avaliação deve ser um inteiro de 0 a 10")

    @property
    def comentario(self):
        return self._comentario
    @comentario.setter
    def comentario(self, novo_comentario):
        if novo_comentario is None:
            self._comentario = None
        if len(novo_comentario) > 0 and len(novo_comentario) > novo_comentario.count(" "):
            self._comentario = novo_comentario
        else:
            raise ValueError("O novo comentário não pode ser vazio")

        
    def alterar_nota(self, nova_nota):
        self.nota = nova_nota

    def alterar_comentario(self, novo_comentario):
        self.comentario = novo_comentario