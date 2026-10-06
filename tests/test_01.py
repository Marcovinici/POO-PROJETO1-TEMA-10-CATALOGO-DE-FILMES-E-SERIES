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
    # Confirma que a avaliação válida é salva como nota do filme.
    filme = teste.Filme("Poderoso Chefão", 1, 2026, "Livre")
    filme.avaliar_filme(4.5)
    assert filme.__dict__ == {'_titulo': 'Poderoso Chefão', 'genero': None, '_duracao': 1, '_ano': 2026, '_classificacao': 'LIVRE', 'elenco': [], 'diretor': [], 'roteirista': [], '_status': 'NAO-ASSISTIDO', '_nota': 4.5, 'avaliacoes': [4.5]}


def test_criarFilme_nota_invalida():
    # Rejeita notas acima do limite máximo permitido.
    filme = teste.Filme("Poderoso Chefão", 1, 2026, "Livre")
    with pytest.raises(ValueError, match="nota"):
        filme.nota = 5.1