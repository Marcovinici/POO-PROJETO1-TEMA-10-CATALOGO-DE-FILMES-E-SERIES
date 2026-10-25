class Lista:
    """Representa uma lista personalizada de mídias

    Esta classe organiza mídias selecionadas pelo usuário e permite
    criar a lista, adicionar mídias e removê-las.

    Attributes:
    nome_da_lista (str): Representa o nome da lista
    midias (list[Midia]): Lista contendo as mídias adicionadas
    """
    def __init__(self, nome_da_lista):
        self.nome_da_lista = nome_da_lista
        self.midias = []

    def adicionar_na_lista(self):
        pass

    def remover_da_lista(self):
        pass


class ListaPersonalizada(Lista):
    
    pass