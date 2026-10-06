import modelos.midias
import pytest

teste = modelos.midias

# Testes de Midia

def test_criarMidia():
    # Confirma a criação da mídia com os valores e padrões esperados.
    midia = teste.Midia("Poderoso Chefão", 1, 2026, "Livre")
    assert midia.__dict__ == {'_titulo': 'Poderoso Chefão', 'genero': None, '_duracao': 1, '_ano': 2026, '_classificacao': 'LIVRE', 'elenco': [], 'diretor': [], 'roteirista': [], '_status': 'NAO-ASSISTIDO'}


def test_criarMidia_titulo_invalido():
    # Rejeita títulos vazios ou formados apenas por espaços.
    with pytest.raises(ValueError, match="titulo"):
        midia1 = teste.Midia("   ", 1, 2014, "Livre")


def test_criarMidia_duracao_invalida():
    # Rejeita duração igual a zero.
    with pytest.raises(ValueError, match="duracao"):
        teste.Midia("Poderoso Chefão", 0, 2014, "Livre")


def test_criarMidia_ano_invalido():
    # Rejeita ano de lançamento fora do intervalo permitido.
    with pytest.raises(ValueError, match="ano"):
        teste.Midia("Poderoso Chefão", 1, 1800, "Livre")


def test_criarMidia_classificacao_invalida():
    # Rejeita classificações que não estão entre as opções aceitas.
    with pytest.raises(ValueError, match="classificacao"):
        teste.Midia("Poderoso Chefão", 1, 2014, "Classificação inválida")


def test_criarMidia_status_invalido():
    # Rejeita status que não pertence aos valores permitidos.
    midia = teste.Midia("Poderoso Chefão", 1, 2014, "Livre")
    with pytest.raises(ValueError, match="status"):
        midia.status = "PENDENTE"


@pytest.mark.parametrize("atributo", ["elenco", "diretor", "roteirista"])
def test_criarMidia_atributo_de_lista_invalido(atributo):
    # Rejeita valores que não são listas nos atributos de elenco e equipe.
    atributos = {atributo: "não é uma lista"}
    with pytest.raises(TypeError, match=atributo):
        teste.Midia("Poderoso Chefão", 1, 2014, "Livre", **atributos)

# Testes de Filme

def test_criarFilme():
    # Cria objeto da classe Filme e verifica se os atributos estão com o estado esperado
    filme = teste.Filme("Poderoso Chefão", 1, 2026, "Livre")
    filme.avaliar_filme(4.5)
    assert filme.__dict__ == {'_titulo': 'Poderoso Chefão', 'genero': None, '_duracao': 1, '_ano': 2026, '_classificacao': 'LIVRE', 'elenco': [], 'diretor': [], 'roteirista': [], '_status': 'NAO-ASSISTIDO', '_nota': 4.5, 'avaliacoes': [4.5]}


def test_criarFilme_nota_invalida():
    # Rejeita notas acima do limite máximo permitido.
    filme = teste.Filme("Poderoso Chefão", 1, 2026, "Livre")
    with pytest.raises(ValueError, match="nota"):
        filme.nota = 5.1

# Testes de Serie

def test_criarSerie():
    # Confirma os atributos exclusivos e os valores padrão de uma série.
    episodio = teste.Episodio("Episódio", 30, 2020, "Livre", 1)
    temporada = teste.Temporada(1, [episodio])
    serie = teste.Serie("Série", 30, 2020, "Livre", temporadas=[temporada])

    assert serie.temporadas == [temporada]
    assert serie.total_temporadas == 1
    assert serie.total_episodios == 1
    assert serie.nota_serie is None
    assert serie.avaliacoes == []
    serie.nota_serie = 4.5
    assert serie.nota_serie == 4.5


@pytest.mark.parametrize("temporadas", ["não é uma lista", [object()]])
def test_criarSerie_temporadas_invalidas(temporadas):
    # Rejeita temporadas que não sejam uma lista de objetos Temporada.
    with pytest.raises(TypeError):
        teste.Serie("Série", 30, 2020, "Livre", temporadas=temporadas)


@pytest.mark.parametrize("nota", [-0.1, 5.1])
def test_criarSerie_nota_invalida(nota):
    # Rejeita notas da série fora do intervalo de zero a cinco.
    serie = teste.Serie("Série", 30, 2020, "Livre")
    with pytest.raises(ValueError, match="nota"):
        serie.nota_serie = nota


# Testes de Temporada

def test_criarTemporada():
    # Confirma o número, a lista de episódios, a contagem e os valores padrão.
    episodio = teste.Episodio("Episódio", 30, 2020, "Livre", 1)
    temporada = teste.Temporada(1, [episodio])

    assert temporada.numero == 1
    assert temporada.episodios == [episodio]
    assert temporada.total_episodios == 1
    assert temporada.nota_temporada is None
    assert temporada.avaliacoes == []
    temporada.nota_temporada = 4.5
    assert temporada.nota_temporada == 4.5


@pytest.mark.parametrize("numero", [0, -1])
def test_criarTemporada_numero_invalido(numero):
    # Rejeita números de temporada menores ou iguais a zero.
    with pytest.raises(ValueError, match="numero"):
        teste.Temporada(numero)


@pytest.mark.parametrize("episodios", ["não é uma lista", [object()]])
def test_criarTemporada_episodios_invalidos(episodios):
    # Rejeita episódios que não sejam uma lista de objetos Episodio.
    with pytest.raises(TypeError, match="episodios|Episodio"):
        teste.Temporada(1, episodios)


@pytest.mark.parametrize("nota", [-0.1, 5.1])
def test_criarTemporada_nota_invalida(nota):
    # Rejeita notas da temporada fora do intervalo de zero a cinco.
    temporada = teste.Temporada(1)
    with pytest.raises(ValueError, match="nota"):
        temporada.nota_temporada = nota


# Testes de Episodio

def test_criarEpisodio():
    # Confirma os atributos exclusivos e os valores padrão de um episódio.
    episodio = teste.Episodio("Episódio", 30, 2020, "Livre", 1)

    assert episodio.numero == 1
    assert episodio.nota is None
    assert episodio.avaliacoes == []
    episodio.nota = 4.5
    assert episodio.nota == 4.5


@pytest.mark.parametrize("numero", [0, -1])
def test_criarEpisodio_numero_invalido(numero):
    # Rejeita números de episódio menores ou iguais a zero.
    with pytest.raises(ValueError, match="numero"):
        teste.Episodio("Episódio", 30, 2020, "Livre", numero)


@pytest.mark.parametrize("nota", [-0.1, 5.1])
def test_criarEpisodio_nota_invalida(nota):
    # Rejeita notas do episódio fora do intervalo de zero a cinco.
    episodio = teste.Episodio("Episódio", 30, 2020, "Livre", 1)
    with pytest.raises(ValueError, match="nota"):
        episodio.nota = nota