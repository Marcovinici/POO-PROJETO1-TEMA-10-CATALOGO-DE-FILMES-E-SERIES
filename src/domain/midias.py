from .mixins import AvaliavelMixin
from .excecoes import DadosInvalidosError
from datetime import date

class Midia():
    """Classe base para qualquer tipo de mídia presente no catálogo

    Possui os atributos e métodos comuns a todos objetos de classes que representam mídias

    Attributes:
    titulo (str): Representa o titulo da mídia
    ano (int): Representa a data de lançamento da mídia
    classificacao (str): Representa a classificação de idade recomendada para os indivíduos que conumiram a mídia
    genero (str): Representa o gênero da mídia
    elenco (list[str]): Lista que contém os nomes(strings) que fazem  parte do elenco da mídia
    diretor (list[str]): Lista que guarda o(s) nome(s) do(s) diretor(es) da mídia
    roteirista (list[str]): Lista que guarda o(s) nome(s) do(s) roteirista(s)
    """
    def __init__(self, titulo: str, ano: int, classificacao: str, genero: str = None, elenco: list[str] = None, diretor: list[str] = None, roteirista: list[str] = None):
        
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.classificacao = classificacao

        # Validação de elenco
        if elenco is None:
            self.elenco = []
        elif isinstance(elenco, list):
            self.elenco = elenco
        else:
            raise DadosInvalidosError("O atributo 'elenco' deve ser uma lista de strings")
        # Validação de diretor
        if diretor is None:
            self.diretor = []
        elif isinstance(diretor, list):
            self.diretor = diretor
        else:
            raise DadosInvalidosError("O atributo 'diretor' deve ser uma lista de strings")
        # Validação de roteirista
        if roteirista is None:
            self.roteirista = []
        elif isinstance(roteirista, list):
            self.roteirista = roteirista
        else:
            raise DadosInvalidosError("O atributo 'roteirista' deve ser uma lista de strings")

    # Getter e validação de titulo
    @property
    def titulo(self):
        return self._titulo
    @titulo.setter
    def titulo(self, novo_titulo):
        if len(novo_titulo) > 0 and len(novo_titulo) != novo_titulo.count(" "): # Validade que o título não está vazio
            self._titulo = novo_titulo
        else:
            raise DadosInvalidosError("O titulo não poder estar vazio ou ser apenas espaços em branco")

    # Getter e validação de ano
    @property
    def ano(self):
        return self._ano
    @ano.setter
    def ano(self, novo_ano):
        if 1800 <= novo_ano <= date.today().year + 1: # Garante que a data de lançamento do filme está entre 1800 e o ano atual 
            self._ano = novo_ano
        else:
            raise DadosInvalidosError("O ano de lançamento do filme deve estar entre 1800 e hoje")

    # Getter e validação de classificação
    @property
    def classificacao(self):
        return self._classificacao
    @classificacao.setter
    def classificacao(self, nova_classificacao):
        if nova_classificacao is not isinstance(nova_classificacao, str): # Verifica se nova_classificacao é str
            raise DadosInvalidosError("A classificacao deve ser do tipo 'str'")
        if nova_classificacao.upper() in ["LIVRE", "+6", "+10", "+12", "+16", "+18"]: # Verifica se nova_classificacao é um dos itens (válidos) da lista
            self._classificacao = nova_classificacao.upper()
        else:
            raise DadosInvalidosError("A classificacao deve ser uma das seguintes: 'LIVRE', '+6', '+10', '+12', '+16', '+18'")

    def exibir_detalhes(self):
        """Exibe os valores de cada atributo da mídia"""
        for atributo, valor in self.__dict__.items():
            print(f"{atributo} : {valor}")




class Filme(AvaliavelMixin, Midia):
    """Representa o filme de um catálogo

    Esta classe herda de Midia e representa as mídias do tipo filme

    Attributes
    duracao(int): Representa a duração do conteúdo
    """
    def __init__ (self, titulo: str, duracao: int, ano: int, classificacao: str, genero: str = None, elenco: list[str] = None, diretor: list[str] = None, roteirista: list[str] = None):

        super().__init__(titulo, ano, classificacao, genero, elenco, diretor, roteirista)
        
        self.duracao = duracao

    # Getter e validação de duracao
    @property
    def duracao(self):
        return self._duracao
    @duracao.setter
    def duracao(self, nova_duracao):
        if nova_duracao > 0 and isinstance(nova_duracao, int) and not isinstance(nova_duracao, bool): # Checa se duracao é um inteiro maior que 0
            self._duracao = nova_duracao
        else:
            raise DadosInvalidosError("A duracao não pode ser igual o menor a 0")

    def __repr__(self):
        return f"Filme(titulo = {self.titulo}, duracao = {self.duracao}, ano = {self.ano},\nclassificacao = {self.classificacao}, genero = {self.genero}, elenco = {self.elenco},\ndiretor = {self.diretor}, roteirista = {self.roteirista}, nota = {self.nota_media})"




class Episodio(AvaliavelMixin, Midia):
    """Representa um episódio que pertence a uma temporada de uma série do catálogo

    Esta classe herda de Midia e possui atributos e métodos próprios de episódios. Um objeto dessa classe depende da existência de uma temporada
    
    Attributes:
    duracao (int): Representa a duração do conteúdo
    numero (int): Representa o número do episódio
    avaliacoes (list[Avaliacao]): Lista contendo as avaliações do episódio
    """
    def __init__(self, titulo: str, duracao: int, ano: int, classificacao: str, numero: int, genero: str = None, elenco: list[str] = None, diretor: list[str] = None, roteirista: list[str] = None):
        
        super().__init__(titulo, ano, classificacao, genero, elenco, diretor, roteirista)

        self.duracao = duracao
        self.numero = numero

    # Getter e validação de duracao
    @property
    def duracao(self):
        return self._duracao
    @duracao.setter
    def duracao(self, nova_duracao):
        if nova_duracao > 0 and isinstance(nova_duracao, int) and not isinstance(nova_duracao, bool): # Checa se duracao é um inteiro maior que 0
            self._duracao = nova_duracao
        else:
            raise DadosInvalidosError("A duracao não pode ser igual o menor a 0")

    # Getter e validação de numero
    @property
    def numero(self):
        return self._numero
    @numero.setter
    def numero(self, numero):
        if numero > 0 and isinstance(numero, int) and not isinstance(numero, bool): # Checa se numero é um inteiro maior que 0
            self._numero = numero
        else:
            raise DadosInvalidosError("O atributo 'numero' deve ser um número inteiro maior que 0")
 
    def __repr__(self):
        return f"Episodio(titulo = {self.titulo}, duracao = {self.duracao}, ano = {self.ano},\nclassificacao = {self.classificacao}, genero = {self.genero}, elenco = {self.elenco},\ndiretor = {self.diretor}, roteirista = {self.roteirista}, numero = {self.numero}, nota = {self.nota_media})"




class Temporada(AvaliavelMixin):
    """Representa uma temporada pertencente a uma série do catálogo
    
    Esta classe funciona como um agrupador de episódios e depende da existência de uma série

    Attributes:
    numero (int): Representa o número correspondente da temporada
    episodios (list[Episodio]): Lista contendo os episódios que pertencem a temporada
    total_episodios (int): Representa o número total de episódios da temporada
    nota_media_episodios (float): Representa a média de notas de todos os episódios da temporada
    nota_temporada (float): Representa a nota da temporada
    avaliacoes (list[Avaliacao]): Lista contendo as avaliacoes da temporada
    """
    def __init__(self, numero: int, episodios: list["Episodio"] = None):
        super().__init__()
        self.numero = numero
        self.episodios = episodios

    # Getter e validação de numero
    @property
    def numero(self):
        return self._numero
    @numero.setter
    def numero(self, numero):
        if numero > 0 and isinstance(numero, int) and not isinstance(numero, bool): # Checa se numero é um inteiro maior que 0
            self._numero = numero
        else:
            raise DadosInvalidosError("O atributo 'numero' deve ser um número maior que 0")

    # Getter e validação de episodios
    @property
    def episodios(self):
        return self._episodios
    @episodios.setter
    def episodios(self, episodios):
        if episodios is None: # Se episodios é None, deixa episodios como uma lista vazia
            self._episodios = []
        elif isinstance(episodios, list): # Se for uma lista, checa se todos os elemntos são instâncias de Episodio
            if all(isinstance(item, Episodio) for item in episodios):
                self._episodios = episodios
            else:
                raise DadosInvalidosError("Todos os items da lista 'episodios' devem ser objetos da classe Episodio")
        else:
            raise DadosInvalidosError("O atributo 'episodios' deve ser uma lista")

    # Getter do total de episódios
    @property
    def total_episodios(self):
        return len(self.episodios)

    
    def __repr__(self):
        return f"Temporada(numero = {self.numero}, episodios = {self.episodios}, _total_episodios = {self.total_episodios}, _nota_media = {self.nota_media}, avaliacoes = {self.avaliacoes})"

    def __len__(self):
        return len(self.episodios)

    def mostrar_episodios(self):
        return self.episodios




class Serie(AvaliavelMixin, Midia):
    """Representa uma série de TV/Streaming presente no catálogo

    Esta classe herda de Midia e possui atributos e métodos próprios para séries do catálogo

    Attributes:
    temporadas (list[Temporada]): Lista contendo as temporadas da série
    nota_media_temparadas (float): Representa média das notas de cada temporada --> AvaliavelMixin
    total_temporadas (int): Representa o número total de temporadas da série
    total_episodios (int): Representa o número total de episódios da série
    """
    def __init__(self, titulo: str, ano: int, classificacao: str, genero: str = None, elenco: list[str] = None, diretor: list[str] = None, roteirista: list[str] = None, temporadas: list["Temporada"] = None):
        
        super().__init__(titulo, ano, classificacao, genero, elenco, diretor, roteirista)
        self.temporadas = temporadas

    # Getter e validação de temporadas
    @property
    def temporadas(self):
        return self._temporadas
    @temporadas.setter
    def temporadas(self, temporadas):
        if temporadas is None: # Se o argumento de temporadas é None, temporadas receberá uma lista vazia
            self._temporadas = []
        elif isinstance(temporadas, list): # Se o argumento de temporadas é uma lista e seus elemtos são instâncias de Temporada, temporadas receberá essa lista
            if all(isinstance(item, Temporada) for item in temporadas):
                self._temporadas = temporadas
            else:
                raise DadosInvalidosError("Todos os items presentes na lista de 'temporadas' devem ser objetos da classe Temporada")
        else:
            raise DadosInvalidosError("O atributo 'temporadas' deve ser uma lista de objetos Temporada")

    # Getter do total de temporadas
    @property
    def total_temporadas(self):
        return len(self.temporadas)

    # Getter do total de episódios
    @property
    def total_episodios(self):
        return sum(temporada.total_episodios for temporada in self.temporadas)
            
    def __repr__(self):
        return f"Serie(titulo = {self.titulo}, ano = {self.ano},\nclassificacao = {self.classificacao}, genero = {self.genero}, elenco = {self.elenco},\ndiretor = {self.diretor}, roteirista = {self.roteirista}, temporadas = {self.temporadas}, nota = {self.nota_media}, total_temporadas = {self.total_temporadas}, total_episodios = {self.total_episodios})"

    def ver_temporadas(self):
        return self.temporadas
