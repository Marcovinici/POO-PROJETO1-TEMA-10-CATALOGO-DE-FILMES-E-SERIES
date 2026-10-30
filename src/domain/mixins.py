from .avaliacao import Avaliacao
from .excecoes import DadosInvalidosError


class AvaliavelMixin:
    """Mixin com a função de permitir que a mídia possa receber avaliações e manipular as mesmas"""

    @property
    def avaliacoes(self) -> list[Avaliacao]:
        """Inicializa a lista apenas quando for acessada."""
        if not hasattr(self, "_avaliacoes"): # Caso a mídia não possua uma lista de avaliações, será criada uma lista vazia
            self._avaliacoes: list[Avaliacao] = []
        return self._avaliacoes

    def avaliar(self, avaliacao: Avaliacao) -> None:
        """Adiciona uma nova avaliação."""
        if isinstance(avaliacao, Avaliacao): # Só guarda na lista objetos da classe Avaliacao
            self.avaliacoes.append(
                avaliacao
            )  # Usa o property que já garante a existência da lista
        else:
            raise DadosInvalidosError("Deve ser uma instância de Avaliacao.")

    @property
    def nota_media(self) -> float | None:
        """Calcula a nota média."""
        if not self.avaliacoes: # Se não há avaliações, não é feito a média
            return None
        return round(sum(a.nota for a in self.avaliacoes) / len(self.avaliacoes), 1) # round(x, 1) arredonda o valor para uma só casa após a vírgula