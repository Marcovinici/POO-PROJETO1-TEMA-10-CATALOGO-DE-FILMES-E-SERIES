import argparse
from repositories.sessao import Sessao
from domain.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from domain.midias import Filme, Serie
from repositories.filme_repository import FilmeRepository
from repositories.serie_repository import SerieRepository
from domain.listas import ListaPersonalizada
from repositories.listas_repository import ListasRepository


# Instanciando os repositórios
repo_usuario = UsuarioRepository("src/database/banco.db")
sessao = Sessao("src/database/banco.db")
repo_filme = FilmeRepository("src/database/banco.db")
repo_serie = SerieRepository("src/database/banco.db")
repo_listas = ListasRepository("src/database/banco.db")

# --------------------FUNÇÕES-----------------------
def logar(args):
    if repo_usuario.login(args.nome_de_usuario, args.senha):
        sessao.registrar_login(args.nome_de_usuario)
        print(f"O usuario {args.nome_de_usuario} foi logado com sucesso!")
    else:
        print("Nome de usuário ou senha inválidas")
    
def cad_usuario(args):
    if args.admin :
        novo_usuario = Usuario(args.nome_de_usuario, args.senha, args.nome, "ADMIN")
    else:
        novo_usuario = Usuario(args.nome_de_usuario, args.senha, args.nome)
    print(repo_usuario.cadastrar(novo_usuario))

# FUNÇOES DE USUÁRIO PADRAO
def usuario(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        print(f"Usuário: {usuario.nome_de_usuario}; nome: {usuario.nome}; tipo: {usuario.tipo}")
    else:
        print("Nenhum usuário logado")

def logout(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        sessao.encerrar_sessao()
    else:
        print("Não há usuário logado")

# FUNÇÕES DE ADMIN
def listar_usuarios(args):
    usuario = sessao.obter_usuario_logado()
    if usuario:
        if usuario.tipo == "ADMIN":
            linhas = repo_usuario.listar()
            for linha in linhas:
                print(linha)
        else:
            print(f"O usuário '{usuario.nome_de_usuario}' não tem permissão de administrador")
    else:
        print("O usuário não está logado")

# -------------------------------------MAIN---------------------------------------
def main():
    parser = argparse.ArgumentParser(
    prog= "Catalogo de Midias CLI",
    description= "Programa para manipular e gerenciar um catálogo de filmes e séries"
    )

    # CRIA O GESTOR DE SUBCOMANDOS
    subparsers = parser.add_subparsers(
        dest="comando",  # Guarda o nome do comando digitado em args.comando
        required=True,  # Obriga o utilizador a escolher um comando
    )

    # CRIA OS COMANDOS

    # Comando 'logar'
    cmd_logar = subparsers.add_parser(
        "logar", help="O usuário pode logar adicionando o 'nome de usuário' e a 'senha' como argumentos"
    )
    cmd_logar.add_argument("nome_de_usuario", type=str, help="Nome de usuário")
    cmd_logar.add_argument("senha", type=str, help="Senha do usuário")

    cmd_logar.set_defaults(func=logar)
    # Comando 'cadastrar'
    cmd_cad_usuario = subparsers.add_parser(
        "cad-usuario", help="O usuário pode cadastrar um nomvo usuario"
    )
    cmd_cad_usuario.add_argument("nome_de_usuario", type=str, help="Nome de usuário")
    cmd_cad_usuario.add_argument("senha", type=str, help="Senha do usuário")
    cmd_cad_usuario.add_argument("nome", type=str, help="Nome real do usuário")
    cmd_cad_usuario.add_argument("--admin", action="store_true", help="Define o usuário como Administrador")

    cmd_cad_usuario.set_defaults(func=cad_usuario)

    # COMANDOS DE USUÁRIO LOGADO

    # Comando usuario
    cmd_usuario = subparsers.add_parser(
        "usuario", help="Imprime informações sobre o usuario que está logado no momento"
    )

    cmd_usuario.set_defaults(func=usuario)

    # Comando logout
    cmd_logout = subparsers.add_parser(
        "logout", help="Desloga o usuario"
    )

    cmd_logout.set_defaults(func=logout)


    # COMANDOS DE USUÁRIO ADMINISTRADOR
    cmd_listar_usuarios = subparsers.add_parser(
        "listar-usuarios", help="O comando imprime todos os usuários cadastrados (esse comando só está disponível para administradores)"
    )

    cmd_listar_usuarios.set_defaults(func=listar_usuarios)

    # LENDO ARGS
    args = parser.parse_args()

    # LIGANDO ARGS A FUNÇOES
    args.func(args)

if __name__ == "__main__":
    main()