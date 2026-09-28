class Midia:
    """Classe base para qualquer tipo de mídia presente no catálogo

    Possui os atributos e métodos comuns a todos objetos de classes que representam mídias

    Attributes:
    titulo (str): Representa o titulo da mídia
    genero (str): Representa o gênero da mídia
    ano (int): Representa a data de lançamento da mídia
    duracao (int): Representa a duração do conteúdo
    classificacao (str): Representa a classificação de idade recomendada para os indivíduos que conumiram a mídia
    status (str): Guarda a informação que indica se a midia foi reproduzida ou não pelo usuário
    elenco (list[str]): Lista que contém os nomes(strings) que fazem  parte do elenco da mídia
    diretor (list[str]): Lista que guarda o(s) nome(s) do(s) diretor(es) da mídia
    roteirista (list[str]): Lista que guarda o(s) nome(s) do(s) roteirista(s) 
    """
    def __init__(self, titulo = None, duracao = None, ano = None):
        pass

    def exibir_detalhes(self):
        pass
    def alterar_status(self):
        pass



class Filme(Midia):
    """Representa o filme de um catálogo

    Esta classe herda de Midia e possui atributos e métodos extras próprio dos filmes do catálogo

    Attributes:
    nota (float): Representa a nota do filme
    avaliacoes (list[Avaliacao]): Lista contendo as avaliações do filme
    """
    def __init__ (self):
        pass

    def avaliar_filme(self):
        pass
    def ver_avaliacoes(self):
        pass



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