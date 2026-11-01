# Classe base para todas as exceções
class CatalogoError(Exception):
    """Exceção base para qualquer erro de negócio do catálogo."""

    pass

# Falha de validação
class DadosInvalidosError(CatalogoError):
    """Lançada quando qualquer atributo recebe um dado inválido (ex: ano, duração, nota, título vazio)."""

    pass

# Erros no cdastro

class ItemNaoEncontradoError(CatalogoError):
    """Lançada quando um filme, série, lista ou usuário não é encontrado."""

    pass


class ItemDuplicadoError(CatalogoError):
    """Lançada ao tentar cadastrar uma mídia ou lista que já existe."""

    pass