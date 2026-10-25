import argparse
from .. domain.usuario import Usuario
from .. repositories.usuario_repository import UsuarioRepository

repo_usuario = UsuarioRepository("src/database/banco.db")

def logar(args):
    print(repo_usuario.login(args.nome_de_usuario, args.senha))
    repo_usuario.existe_usuario(args.nome_de_usuario)
    
def cadastrar_usuario(args):
    if args.admin :
        novo_usuario = Usuario(args.nome_de_usuario, args.senha, args.nome, "ADMINISTRADOR")
    else:
        novo_usuario = Usuario(args.nome_de_usuario, args.senha, args.nome)
    print(repo_usuario.cadastrar(novo_usuario))

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

    cmd_cad_usuario.set_defaults(func=cadastrar_usuario)

    # COMANDOS DE USUÁRIO ADMINISTRADOR
    

    # LENDO ARGS
    args = parser.parse_args()

    # LIGANDO ARGS A FUNÇOES
    args.func(args)

if __name__ == "__main__":
    main()