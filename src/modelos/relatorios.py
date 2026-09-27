class Relatorio:
    """Classe base para os relatórios do catálogo

    Esta classe reúne os dados de identificação e as operações comuns
    aos relatórios.

    Attributes:
    nome_do_usuario (str): Representa o nome do usuário do relatório
    nome_do_relatorio (str): Representa o nome do relatório
    """
    def __init__(self):
       pass

    def criar_relatorio(self):
        pass
    def atualizar_relatorio(self):
        pass
    def mostrar_relatorio(self):
        pass



class RelatorioGeral(Relatorio):
    """Representa o relatório geral de consumo do usuário

    Esta classe herda de Relatorio e reúne estatísticas e seleções
    relacionadas às mídias do catálogo.

    Attributes:
    media_notas_por_genero (float): Representa a média das notas por gênero
    tempo_total_assistido (float): Representa o tempo total de consumo de mídias
    top10_bem_avaliados (list): Lista das dez mídias mais bem avaliadas
    series_mais_eps_assistidos (list): Lista contendo as séries com mais episódios assistidos
    filmes_mais_assistidos (list): Lista contendo os filmes mais assistidos
    series_mais_assistidas (list): Lista contendo as séries mais assistidas
    """
    def __init__(self):
        pass



class RelatorioHistorico(Relatorio):
    """Representa o relatório de consumo baseado no histórico

    Esta classe herda de Relatorio e organiza o tempo de consumo em
    diferentes períodos.

    Attributes:
    tempo_total_dia (float): Representa o tempo total assistido no dia
    tempo_total_semana (float): Representa o tempo total assistido na semana
    tempo_total_mes (float): Representa o tempo total assistido no mês
    """
    def __init__(self):
        pass