class Usuario:
    """Representa o usuário do catálogo de mídias

    Esta classe guarda os dados de identificação do usuário e permite
    alterar seu nome de usuário e sua senha.

    Attributes:
    nome_de_usuario (str): Representa o nome de usuário usado para identificação
    nome (str): Representa o nome real do usuário
    senha (str): Representa a senha do usuário
    tipo(str): Representa o tipo de usuário (padrão ou adiministrador)
    """
    def __init__(self, nome_de_usuario, senha, nome, tipo = "PADRAO"):
        self.nome_de_usuario = nome_de_usuario
        self.senha = senha
        self.nome = nome
        self.tipo = tipo

    @property
    def nome_de_usuario(self):
        return self.nome_de_usuario
    @nome_de_usuario.setter
    def nome_de_usuario(self, novo_nome):
        if 0 < len(novo_nome) <= 100:
            self.nome_de_usuario = novo_nome
        else:
            raise ValueError("O nome de usuário deve ter entre 1 e 100 caracteres")

    @property
    def senha(self):
        return self.senha
    @senha.setter
    def senha(self, nova_senha):
        if len(nova_senha) > 4:
            self.senha = nova_senha
        else:
            raise ValueError("A senha deve possuir ao menos 4 caracteres")

    @property
    def nome(self):
        return self.nome
    @nome.setter
    def nome(self, novo_nome):
        if len(novo_nome) > novo_nome.count(" ") and len(novo_nome) > 0:
            self.nome = novo_nome
        else:
            raise ValueError("O nome não pode ser vazio")

    
    def mudar_nome_de_usuario(self, novo_nome):
        self.nome_de_usuario = novo_nome

    def mudar_senha(self, nova_senha):
        self.senha = nova_senha