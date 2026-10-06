class Midia:
    """Classe base para qualquer tipo de mídia presente no catálogo

    Possui os atributos e métodos comuns a todos objetos de classes que representam mídias

    Attributes:
    titulo (str): Representa o titulo da mídia
    ano (int): Representa a data de lançamento da mídia
    duracao (int): Representa a duração do conteúdo
    classificacao (str): Representa a classificação de idade recomendada para os indivíduos que conumiram a mídia
    genero (str): Representa o gênero da mídia
    status (str): Guarda a informação que indica se a midia foi reproduzida ou não pelo usuário
    elenco (list[str]): Lista que contém os nomes(strings) que fazem  parte do elenco da mídia
    diretor (list[str]): Lista que guarda o(s) nome(s) do(s) diretor(es) da mídia
    roteirista (list[str]): Lista que guarda o(s) nome(s) do(s) roteirista(s) 
    """
    def __init__(self, titulo: str, duracao: int, ano: int, classificacao: str, genero: str = None, elenco: list[str] = None, diretor: list[str] = None, roteirista: list[str] = None):
        self.titulo = titulo
        self.genero = genero
        self.duracao = duracao
        self.ano = ano
        self.classificacao = classificacao
        # Validação de elenco
        if elenco is None:
            self.elenco = []
        elif isinstance(elenco, list):
            self.elenco = elenco
        else:
            raise TypeError("O atributo 'elenco' deve ser uma lista de strings")
        # Validação de diretor
        if diretor is None:
            self.diretor = []
        elif isinstance(diretor, list):
            self.diretor = diretor
        else:
            raise TypeError("O atributo 'diretor' deve ser uma lista de strings")
        # Validação de roteirista
        if roteirista is None:
            self.roteirista = []
        elif isinstance(roteirista, list):
            self.roteirista = roteirista
        else:
            raise TypeError("O atributo 'roteirista' deve ser uma lista de strings")
        self._status = "NAO-ASSISTIDO"

    @property
    def titulo(self):
        return self._titulo
    @titulo.setter
    def titulo(self, novo_titulo):
        if len(novo_titulo) > 0 and len(novo_titulo) != novo_titulo.count(" "):
            self._titulo = novo_titulo
        else:
            raise ValueError("O titulo não poder estar vazio ou ser apenas espaços em branco")

    @property
    def duracao(self):
        return self._duracao
    @duracao.setter
    def duracao(self, nova_duracao):
        if nova_duracao > 0:
            self._duracao = nova_duracao
        else:
            raise ValueError("A duracao não pode ser igual o menor a 0")

    @property
    def ano(self):
        return self._ano
    @ano.setter
    def ano(self, novo_ano):
        if 1800 < novo_ano <= 2026:
            self._ano = novo_ano
        else:
            raise ValueError("O ano de lançamento do filme deve entre 1800 e 2026")

    @property
    def classificacao(self):
        return self._classificacao
    @classificacao.setter
    def classificacao(self, nova_classificacao):
        if nova_classificacao.upper() in ["LIVRE", "+6", "+10", "+12", "+16", "+18"]:
            self._classificacao = nova_classificacao.upper()
        else:
            raise ValueError("A classificacao deve ser uma das seguintes: 'LIVRE', '+6', '+10', '+12', '+16', '+18'")

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, novo_status):
        if novo_status == "ASSISTIDO" or novo_status == "NAO-ASSISTIDO" or novo_status == "ASSISTINDO":
            self._status = novo_status
        else:
            raise ValueError("O status de uma mídia só pode ser um dos seguintes: ASSISTIDO, NAO-ASSISTIDO ou ASSISTINDO")

    def exibir_detalhes(self):
        for atributo, valor in self.__dict__.items():
            print(f"{atributo} : {valor}")
            
    def alterar_status(self, status: str):
        if self.status == status:
            return f"O objeto {self} continuará com seu status ({self.status}) inalterado"
        else:
            self.status = status
    def __repr__(self):
        return f""

class Filme(Midia):
    """Representa o filme de um catálogo

    Esta classe herda de Midia e possui atributos e métodos extras próprio dos filmes do catálogo

    Attributes:
    nota (float): Representa a nota do filme
    avaliacoes (list[Avaliacao]): Lista contendo as avaliações do filme
    """
    def __init__ (self, titulo: str, duracao: int, ano: int, classificacao: str, genero: str = None, elenco: list[str] = None, diretor: list[str] = None, roteirista: list[str] = None):
        super().__init__(titulo, duracao, ano, classificacao, genero, elenco, diretor, roteirista)
        self._nota = None
        self.avaliacoes = []

    @property
    def nota(self):
        return self._nota
    @nota.setter
    def nota(self, nota):
        if 0 <= nota <= 5:
            self._nota = nota
        else:
            raise ValueError("A nota deve ser um número entre 0 e 5")    

    def __repr__(self):
        return f"Filme(titulo = {self.titulo}, duracao = {self.duracao}, ano = {self.ano},\nclassificacao = {self.classificacao}, genero = {self.genero}, elenco = {self.elenco},\ndiretor = {self.diretor}), roteirista = {self.roteirista}"

    def avaliar_filme(self, nota: float):
        if self.nota != None:
            self.avaliacoes.remove(self.nota)
            self.nota = nota
        else:
            self.nota = nota
            self.avaliacoes.append(nota)

    def ver_avaliacoes(self):
        return self.avaliacoes



class Serie(Midia):
    """Representa uma série de TV/Streaming presente no catálogo

    Esta classe herda de Midia e possui atributos e métodos próprios para séries do catálogo

    Attributes:
    temporadas (list[Temporada]): Lista contendo as temporadas da série
    nota_media (float): Representa média das notas de cada temporada
    nota_serie (float): Representa nota da série
    total_temporadas (int): Representa o número total de temporadas da série
    total_episodios (int): Representa o número total de episódios da série
    avaliacoes (list[Avaliacao]): Lista contendo as avaliações da série
    """
    def __init__(self):
        pass

    def ver_temporadas(self):
        pass
    def avaliar_serie(self):
        pass
    def ver_avaliacoes(self):
        pass
    def media_avaliacao_temporadas(self):
        pass



class Temporada:
    """Representa uma temporada pertencente a uma série do catálogo
    
    Esta classe funciona como um agrupador de episódios e depende da existência de uma série

    Attributes:
    numero (int): Representa o número correspondente da temporada
    episodios (list[Episodio]): Lista contendo os episódios que pertencem a temporada
    total_episodios (int): Representa o número total de episódios da temporada
    nota_media (float): Representa a média de notas de todos os episódios da temporada
    nota_temporada (float): Representa a nota da temporada
    avaliacoes (list[Avaliacao]): Lista contendo as avaliacoes da temporada
    """
    def __init__(self):
        pass

    def media_avaliacao_episodios(self):
        pass
    def avaliar_temporada(self):
        pass
    def mostrar_episodios(self):
        pass
    def ver_avaliacoes(self):
        pass



class Episodio(Midia):
    """Representa um episódio que pertence a uma temporada de uma série do catálogo

    Esta classe herda de Midia e possui atributos e métodos próprios de episódios. Um objeto dessa classe depende da existência de uma temporada
    
    Attributes:
    numero (int): Representa o número do episódio
    nota (float): Possui a nota correspondente do episódio
    avaliacoes (list[Avaliacao]): Lista contendo as avaliações do episódio
    """
    def __init__(self):
        pass
    
    def avaliar_episodio(self):
        pass
    def ver_avaliacoes(self):
        pass