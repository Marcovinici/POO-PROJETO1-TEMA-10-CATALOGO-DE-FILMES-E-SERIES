class ListasPersonalizadas:
    """Representa uma lista personalizada de mídias

    Esta classe organiza mídias selecionadas pelo usuário e permite
    criar a lista, adicionar mídias e removê-las.

    Attributes:
    usuario (str): Guarda o usuário dono da lista
    nome_da_lista (str): Representa o nome da lista
    midias (list[Midia]): Lista contendo as mídias adicionadas
    """
    def __init__(self, nome_da_lista):
        self.nome_da_lista = nome_da_lista
        self.midias = []

    def adicionar_na_lista(self, nova_midia):
        if nova_midia.titulo not in self.midias:
            self.midias.append(nova_midia)
            return f"{nova_midia.titulo} adicionado com sucesso a {self.nome_da_lista}"
        else:
            raise ValueError("A mídia já pertence a lista")
        

    def remover_da_lista(self, midia):
        if midia.titulo not in self.midias:
            raise ValueError(f"A mídia de título {midia.titulo} não pertence a lista {self.nome_da_lista}")
