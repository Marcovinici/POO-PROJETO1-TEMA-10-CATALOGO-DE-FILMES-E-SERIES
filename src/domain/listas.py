class ListaPersonalizada:
    """Representa uma lista personalizada de mídias

    Esta classe organiza mídias selecionadas pelo usuário e permite
    criar a lista, adicionar mídias e removê-las.

    Attributes:
    usuario (str): Guarda o usuário dono da lista
    nome (str): Representa o nome da lista
    id (int): Guarda o id da lista
    midias (list[Midia]): Lista contendo as mídias adicionadas
    """
    def __init__(self, nome_da_lista, usuario, id = None):
        self.nome = nome_da_lista
        self.usuario = usuario
        self.id = id
        self.midias = []

    def adicionar_na_lista(self, nova_midia):
        if any(midia.titulo == nova_midia.titulo for midia in self.midias):
            raise ValueError("A mídia já pertence a lista")

        self.midias.append(nova_midia)
        return f"{nova_midia.titulo} adicionado com sucesso a {self.nome}"
        

    def remover_da_lista(self, midia):
        if midia.titulo not in self.midias:
            raise ValueError(f"A mídia de título {midia.titulo} não pertence a lista {self.nome}")
